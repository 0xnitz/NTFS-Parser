from sector_reader import SectorReader, SECTOR_SIZE
from constants import *
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
        self.mft_last_sector = 0
        self.sector_reader = SectorReader(r'\\.\physicaldrive0')

    def find_mft(self):
        """
        This function reads the boot sector of the file system and locates the start of the MFT
        :return: the starting sector for the MFT
        """

        global SECTOR_SIZE

        # 1161216 is the sector offset of the vbr
        data = self.sector_reader.read_sector(1161216)
        SECTOR_SIZE = struct.unpack('H', data[0xb:0xd])[0]
        self.sectors_per_cluster = data[0xd]
        self.mft_start_sector = 1161216 + struct.unpack('<Q', data[0x30:0x38])[0] * self.sectors_per_cluster

        # Find the last mft sector using the $Mft
        self.mft_last_sector = 0
        self.mft_entry_size = 1024

    def get_next_entry(self):
        """
        This function reads the next mft entry and returns it
        :return: bytes object of an mft entry
        """

        # MFT file not yet found
        if self.mft_start_sector == 0:
            return

        # Finished reading the MFT
        if self.mft_start_sector + self.mft_sector_offset == self.mft_last_sector + 1:
            return READ_ENTIRE_MFT

        # Change to read_until
        # Finding the next file entry in the $MFT
        current_entry, sectors_read = self.sector_reader.read_until(
            self.mft_start_sector + self.mft_sector_offset, b'FILE')
        self.mft_sector_offset += sectors_read

        # If the entry is not allocated or damaged, skip to the next entry
        while not current_entry[0x16] or current_entry[:0x4] != b'FILE':
            current_entry, sectors_read = self.sector_reader.read_until(
                self.mft_start_sector + self.mft_sector_offset, b'FILE')

        self.mft_sector_offset += sectors_read
        self.entry_i += 1

        return current_entry

    def get_entry_size(self):
        """
        :return: The MFT entry size as found in the $MFT entry
        """

        return self.mft_entry_size

    def read_data(self, mft_entry):
        """
        Reads a non-resident $DATA attribute's data from it's run-list
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

        run_list_offset = data_attribute[0x20]
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
            cluster_count = data_attribute[i+1:i+1+cluster_count_length]
            first_cluster = data_attribute[i+1+cluster_count_length:i+1+cluster_count_length+first_cluster_length]

            sector_count = cluster_count
            first_sector = first_cluster

            # Converting the first_cluster bytes into a number
            first_sector = bytes_to_number(first_cluster)

            # Converting the cluster_count bytes into a number
            sector_count = bytes_to_number(cluster_count)

            # Converting between cluster and sectors
            first_sector *= self.sectors_per_cluster
            sector_count *= self.sectors_per_cluster

            # Reading the data from the disk
            non_resident_data += self.sector_reader.read_from(first_sector, sector_count)

            # Jumping to the next cluster run
            i += 1 + cluster_count_length + first_cluster_length

        return non_resident_data
