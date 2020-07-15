from mft_parser import MFTParser
from mft_entry import MFTEntry
from ntfs_handler import NTFSHandler, READ_ENTIRE_MFT
from sector_reader import SectorReader

FAILURE = b'\x01'


class Parser:
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
        current_entry = MFTEntry(b'')

        # Iterating over the MFT and searching for the filename
        while current_entry != READ_ENTIRE_MFT:
            current_entry = MFTEntry(self.handler.get_next_entry())
            if current_entry == filename:
                print('Found it!')
                return current_entry.read_data()

        return FAILURE
