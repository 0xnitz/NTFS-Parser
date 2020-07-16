from attribute_parser import MFTParser
from mft_entry import MFTEntry
from ntfs_handler import *
from sector_reader import SectorReader
from constants import *


class NTFSParser:
    def __init__(self):
        self.mft_parser = MFTParser()
        self.handler = NTFSHandler()
        self.MFT_OFFSET = self.handler.find_mft()

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
            if current_entry == filename:
                return current_entry.read_data()
            current_entry = MFTEntry(self.handler.get_next_entry())

        return FAILURE
