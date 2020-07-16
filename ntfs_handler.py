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
