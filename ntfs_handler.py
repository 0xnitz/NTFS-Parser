from sector_reader import *
from constants import *
from mft_entry import *
import os
import struct


def bytes_to_number(bytes_object):
    """
    This function takes in a bytes object and converts it to a number (1-8 length)
    :param bytes_object: The bytes object to convert
    :return: The result
    """

    bytes_object_length = len(bytes_object)
    n = 0

    if len(bytes_object) > 8:
        return 0

    if bytes_object_length == 1:
        n = bytes_object[0]
    elif bytes_object_length == 2:
        n = struct.unpack('H', bytes_object)[0]
    elif 2 < bytes_object_length <= 4:
        bytes_object += b'\x00' * (4 - bytes_object_length)
        n = struct.unpack('I', bytes_object)[0]
    elif 4 < bytes_object_length <= 8:
        bytes_object += b'\x00' * (8 - bytes_object_length)
        n = struct.unpack('Q', bytes_object)[0]

    return n


class NTFSHandler:
    """
    This class deals with finding the MFT from the VBR and iterating over the MFT to find new entries to parse.
    """

    def __init__(self):
        """
        A constructor for the NTFSHandler class
        """

        self.sectors_per_cluster = 0
        self.mft_entry_size = 0
        self.mft_start_sector = 0
        self.entry_i = 0
        self.mft_sector_offset = 0
        self.runs = []
        self.current_run_index = 0
        self.sector_reader = SectorReader(r'\\.\physicaldrive0')

    def find_mft(self):
        """
        This function reads the boot sector of the file system and locates the start of the MFT
        :return: the starting sector for the MFT
        """

        global SECTOR_SIZE

        data = self.sector_reader.read_sector(VBR_OFFSET)
        SECTOR_SIZE = struct.unpack('H', data[SECTOR_SIZE_OFFSET:SECTOR_SIZE_OFFSET + 2])[0]
        self.sectors_per_cluster = data[SECTORS_PER_CLUSTER_OFFSET]
        self.mft_start_sector = VBR_OFFSET + struct.unpack('<Q',
                                                            data[MFT_START_SECTOR_OFFSET:MFT_START_SECTOR_OFFSET+8])[0]\
                                                            * self.sectors_per_cluster

        # Find the last mft sector using the $Mft
        self.read_data(MFTEntry(self.get_next_entry(no_iteration=True)), index_cluster_runs=True)

    def locate_partition(self):
        """
        This function locates the largest partition and finds it's starting offset
        """

        global VBR_OFFSET

        partitions = os.popen('wmic partition get StartingOffset, Name, Size').read().split('\n')
        partitions = [i for i in partitions if 'Disk' in i]

        max_size = 0
        max_size_offset = 0

        for partition in partitions:
            partition = partition.split()

            if partition[1] == '#0,' and int(partition[4]) > max_size:
                max_size = int(partition[4])
                max_size_offset = int(partition[5])

        VBR_OFFSET = round(max_size_offset / SECTOR_SIZE)

    def get_next_entry(self, no_iteration=False):
        """
        This function reads the next mft entry and returns it
        :arg no_iteration: This argument is used by the find_mft function to get the $MFT entry
        without incrementing self.mft_sector_offset
        :return: bytes object of an mft entry
        """

        # MFT file not yet found
        if self.mft_start_sector == 0:
            return

        # Finding the next file entry in the $MFT
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

        if self.mft_sector_offset >= self.runs[self.current_run_index][1]:
            self.current_run_index += 1
            self.mft_sector_offset = 0

            # Finished reading the MFT
            if self.current_run_index == len(self.runs) and not no_iteration:
                return READ_ENTIRE_MFT

            self.mft_start_sector = self.runs[self.current_run_index][0]

        return current_entry

    def get_entry_size(self):
        """
        :return: The MFT entry size as found in the $MFT entry
        """

        return self.mft_entry_size

    def read_data(self, mft_entry, index_cluster_runs=False):
        """
        Reads a non-resident $DATA attribute's data from it's run-list
        :param index_cluster_runs: This parameter will insert into self.runs
         all of the MFT runs so the program can start iterating over the mft
        :param mft_entry: The MFTEntry object to get the data from
        :return: The non-resident data
        """

        # Cut the $DATA attribute from the entry
        data_attribute = mft_entry.attribute_parser.get_attribute(DATA_TYPE, mft_entry)

        # $DATA attribute not found
        if data_attribute == NO_SUCH_ATTRIBUTE:
            return b''

        # Resident $DATA, call read_resident_data to parse and retrieve it
        if mft_entry.attribute_parser.is_resident(data_attribute):
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
