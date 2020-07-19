from attribute_parser import AttributeParser
from mft_entry import MFTEntry
from ntfs_handler import *
from sector_reader import SectorReader
from constants import *


class NTFSParser:
    """
    This class represents my NTFSParser, it controls all the other objects.
    The parser locates the MFT from the VBR and iterates over it,
    parsing it until it finds an entry with the same filename.
    """

    def __init__(self):
        self.mft_parser = AttributeParser()
        self.handler = NTFSHandler()

        # Locating the largest partition on the disk (C:) and setting VBR_OFFSET to the vbr of C:
        self.handler.locate_partition()

        # Finding the MFT sector offset using the VBR
        self.handler.find_mft()

    def find_file(self, filename):
        """
        This function iterates over every MFT entry and compares it's FILE_NAME to the filename parameter.
        If the program found the right file, it returns it's data attribute
        :param filename:
        :return:
        """

        # Iterating over the MFT and searching for the filename
        current_entry = MFTEntry(self.handler.get_next_entry())
        while len(current_entry.entry) > 0:
            # Using the __eq__ operator of MFTEntry to check if the entry has the correct filename
            if current_entry == filename:
                return self.handler.read_data(current_entry)
            current_entry.entry = self.handler.get_next_entry()

            if current_entry.entry == READ_ENTIRE_MFT:
                break

        # After iterating after the whole MFT, file not found
        return FAILURE
