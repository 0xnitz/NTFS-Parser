from sector_reader import SectorReader, SECTOR_SIZE
from constants import *
import struct


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

        # Add skipping over un-allocated for runtime purpuses
        # allocated = False
        # while not allocated:

        # Change to read_until
        current_entry = self.sector_reader.read_sector(self.mft_start_sector + self.mft_sector_offset)
        self.mft_sector_offset += 1

        next_sector = self.sector_reader.read_sector(self.mft_start_sector + self.mft_sector_offset)
        while b'FILE' != next_sector[:0x4]:
            current_entry += next_sector
            self.mft_sector_offset += 1
            next_sector = self.sector_reader.read_sector(self.mft_start_sector + self.mft_sector_offset)

        self.entry_i += 1

        return current_entry

    def get_entry_size(self):
        """
        :return: The MFT entry size as found in the $MFT entry
        """

        return self.mft_entry_size

    def read_data(self, mft_entry):
        """
        Reads a non-resident $DATA attribute's data from it's runlist
        :param mft_entry: The MFTEntry object to get the data from
        :return: The non-resident data
        """

        # Cut the $DATA attribute from the entry
        data_attribute = mft_entry.attribute_parser.get_attribute(DATA_TYPE, mft_entry)

        # $DATA attribute not found
        if data_attribute == NO_SUCH_ATTRIBUTE:
            return b''

        if mft_entry.attribute_parser.is_resident(data_attribute):
            return mft_entry.read_resident_data()

        run_list_offset = data_attribute[0x20]
        i = run_list_offset
        non_resident_data = b''

        while i < len(data_attribute):
            size = data_attribute[i]
            if size == 0:
                return non_resident_data

            cluster_count_length = size & 0xf
            first_cluster_length = size >> 4

            cluster_count = data_attribute[i+1:i+1+cluster_count_length]
            first_cluster = data_attribute[i+1+cluster_count_length:i+1+cluster_count_length+first_cluster_length]

            sector_count = cluster_count
            first_sector = first_cluster

            if first_cluster_length == 1:
                first_sector = first_cluster[0]
            elif first_cluster_length == 2:
                first_sector = struct.unpack('H', first_cluster)[0]
            elif 2 < first_cluster_length <= 4:
                first_cluster += b'\x00' * (4 - first_cluster_length)
                first_sector = struct.unpack('I', first_cluster)[0]
            elif 4 < first_cluster_length <= 8:
                first_cluster += b'\x00' * (8 - first_cluster_length)
                first_sector = struct.unpack('Q', first_cluster)[0]

            if cluster_count_length == 1:
                sector_count = ord(cluster_count.decode())
            elif cluster_count_length == 2:
                sector_count = struct.unpack('H', cluster_count)[0]
            elif 2 < cluster_count_length <= 4:
                cluster_count += b'\x00' * (4 - cluster_count_length)
                sector_count = struct.unpack('I', cluster_count)[0]
            elif 4 < cluster_count_length <= 8:
                cluster_count += b'\x00' * (8 - cluster_count_length)
                sector_count = struct.unpack('Q', cluster_count)[0]

            first_sector *= self.sectors_per_cluster
            sector_count *= self.sectors_per_cluster

            non_resident_data += self.sector_reader.read_from(first_sector, sector_count)

            i += 1 + cluster_count_length + first_cluster_length

        return non_resident_data
