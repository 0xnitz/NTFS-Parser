from struct import unpack
from os import popen

from constants import SECTOR_SIZE, SECTORS_PER_CLUSTER_OFFSET, SECTOR_SIZE_OFFSET,\
    MFT_START_SECTOR_OFFSET, ENTRY_INUSE, DATA_TYPE, RUN_LIST_OFFSET
from ntfs_exception import ReadEntireMFTException
from attribute_parser import AttributeParser
from sector_reader import SectorReader
from utils import bytes_to_number
from mft_entry import MFTEntry


# CR: [design] This class immediately raises red flags for me for the following
# reasons:
# 1. It has Handler in its name - A generic word that means nothing
# 2. It seems to deal with multiple entities and in many layers of abstraction.
# This contradicts the Single Responsibility Principle. Form what I've seen it
# deals with physical drives, logical partitions, vbrs, mfts, attributes and
# run lists.
# 3. It is very big and has many functions which are too long.
class NTFSHandler:
    """
    This class deals with finding the MFT from the VBR and iterating over the MFT to find new entries to parse.
    """

    # CR: [design] locate_partition and find_mft seem to me like internal
    # functions that should be called by __init__. Why should the client of
    # this class have to call them? What happens if he forgets to? Also, set
    # the attributes in those functions instead of initializing them as 0 which
    # is plainly wrong.
    def __init__(self):
        # CR: [finish] No need for trivial docstrings
        """
        A constructor for the NTFSHandler class
        """

        self.sectors_per_cluster = 0
        self.mft_entry_size = 0
        self.mft_start_sector = 0
        # CR: [finish] This property is only set but never used. Remove
        self.entry_i = 0
        self.mft_sector_offset = 0
        self.runs = []
        self.current_run_index = 0
        # CR: [requirements] Were you required to start from the physical
        # drive?
        self.sector_reader = SectorReader(r'\\.\physicaldrive0')

        NTFSHandler.locate_partition()

        self.find_mft()

    def find_mft(self):
        """
        This function reads the boot sector of the file system and locates the start of the MFT
        :return: the starting sector for the MFT
        """

        # CR: [design] Don't use globals
        global SECTOR_SIZE

        data = self.sector_reader.read_sector(VBR_OFFSET)
        SECTOR_SIZE = unpack('H', data[SECTOR_SIZE_OFFSET:SECTOR_SIZE_OFFSET + 2])[0]
        self.sectors_per_cluster = data[SECTORS_PER_CLUSTER_OFFSET]
        self.mft_start_sector = VBR_OFFSET + unpack('<Q',
                                                            data[MFT_START_SECTOR_OFFSET:MFT_START_SECTOR_OFFSET+8])[0]\
                                                            * self.sectors_per_cluster

        # Find the last mft sector using the $Mft
        self.read_data(MFTEntry(self.get_next_entry(no_iteration=True)), index_cluster_runs=True)

    # CR: [design] This is a good example for a function that can be broken
    # down in the following way:
    # def _largest_partition_vbr_offset(self):
    #    partitions = self._get_partitions()
    #    largest_partition = self._get_largest_partition(partitions)
    #    return self.partition_vbr_offset(largest_partition)
    @staticmethod
    def locate_partition():
        """
        This function locates the largest partition and finds it's starting offset
        """

        # CR: [design] Don't use globals
        global VBR_OFFSET

        # CR: [requirements] Are you allowed to use this?
        partitions = popen('wmic partition get StartingOffset, Name, Size').read().split('\n')
        partitions = [i for i in partitions if 'Disk' in i]

        max_size = 0
        max_size_offset = 0

        for partition in partitions:
            partition = partition.split()

            if partition[1] == '#0,' and int(partition[4]) > max_size:
                max_size = int(partition[4])
                max_size_offset = int(partition[5])

        VBR_OFFSET = round(max_size_offset / SECTOR_SIZE)

    # CR: [implementation] The logic of this function seems unnecessarily
    # complex. Let's talk about it
    def get_next_entry(self, no_iteration=False):
        # CR: [finish] Don't explain what functions use a feature, only what it
        # does.
        # CR: [design] It would be better to eliminate this edge case entirely.
        """
        This function reads the next mft entry and returns it
        :arg no_iteration: This argument is used by the find_mft function to get the $MFT entry
        without incrementing self.mft_sector_offset
        :return: bytes object of an mft entry
        """

        # MFT file not yet found
        # CR: [design] Raise exceptions!
        if self.mft_start_sector == 0:
            return

        # Finding the next file entry in the $MFT
        # CR: [finish] Don't use magic constants, especially ones that repeat
        current_entry, sectors_read = self.sector_reader.read_until(
            self.mft_start_sector + self.mft_sector_offset, b'FILE')
        if no_iteration:
            return current_entry

        self.mft_sector_offset += sectors_read

        # If the entry is not allocated or damaged, skip to the next entry
        while not current_entry[ENTRY_INUSE] or current_entry[:0x4] != b'FILE':
            current_entry, sectors_read = self.sector_reader.read_until(
                self.mft_start_sector + self.mft_sector_offset, b'FILE')
            break

        self.entry_i += 1

        # CR: [design] Why does a function that deals with entries, should
        # need to know about runs, which are 2 abstraction levels deeper?
        if self.mft_sector_offset >= self.runs[self.current_run_index][1]:
            self.current_run_index += 1
            self.mft_sector_offset = 0

            # Finished reading the MFT
            # CR: [design] Raise exceptions!
            if self.current_run_index == len(self.runs) and not no_iteration:
                raise ReadEntireMFTException

            self.mft_start_sector = self.runs[self.current_run_index][0]

        return current_entry

    def get_entry_size(self):
        """
        :return: The MFT entry size as found in the $MFT entry
        """

        return self.mft_entry_size

    # CR: [design] This functions is very long and spans 2-3 missing levels of
    # abstraction.
    def read_data(self, mft_entry, index_cluster_runs=False):
        # CR: [finish] This function also handles resident data, so your
        # docstring is inaccurate
        """
        Reads a non-resident $DATA attribute's data from it's run-list
        :param index_cluster_runs: This parameter will insert into self.runs
         all of the MFT runs so the program can start iterating over the mft
        :param mft_entry: The MFTEntry object to get the data from
        :return: The non-resident data
        """

        # Cut the $DATA attribute from the entry
        data_attribute = AttributeParser.get_attribute(DATA_TYPE, mft_entry)

        # Resident $DATA, call read_resident_data to parse and retrieve it
        if AttributeParser.is_resident(data_attribute):
            return mft_entry.read_resident_data()

        run_list_offset = data_attribute[RUN_LIST_OFFSET]
        i = run_list_offset
        non_resident_data = b''

        # Iterate over the run-list
        while i < len(data_attribute):
            size = data_attribute[i]
            if size == 0:
                return non_resident_data

            # The size is one byte,
            # and it's nibbles represent the amount of bytes the first_cluster and the cluster_length will take
            cluster_count_length = size & 0xf
            first_cluster_length = size >> 4

            # Extracting the cluster_count and first_cluster
            cluster_count = data_attribute[i + 1:i + 1 + cluster_count_length]
            first_cluster = data_attribute[
                            i + 1 + cluster_count_length:i + 1 + cluster_count_length + first_cluster_length]

            # Converting the first_cluster bytes into a number
            first_sector = bytes_to_number(first_cluster)

            # Converting the cluster_count bytes into a number
            sector_count = bytes_to_number(cluster_count)

            # Converting between cluster and sectors
            first_sector *= self.sectors_per_cluster
            sector_count *= self.sectors_per_cluster

            first_sector += VBR_OFFSET

            # Reading the data from the disk
            if not index_cluster_runs:
                non_resident_data += self.sector_reader.read_from(first_sector, sector_count)
            else:
                if i != run_list_offset:
                    self.runs.append((self.runs[-1][0] + first_sector - VBR_OFFSET, sector_count))
                else:
                    self.runs.append((first_sector, sector_count))

            # Jumping to the next cluster run
            i += 1 + cluster_count_length + first_cluster_length

        return non_resident_data
