from mft_entry import MFTEntry, MFT_ENTRY_MAGIC
from ntfs_exception import NTFSException
from sector_reader import SECTOR_SIZE
from mft_loader import MFTLoader

from sys import byteorder


class MFTIterator:
    def __init__(self):
        if byteorder != 'little':
            raise NTFSException

        self.loader = MFTLoader()
        self.mft_offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        mft_length = len(self.loader.mft)

        current_entry = b''
        while True:
            if self.mft_offset >= mft_length:
                self.loader.load_mft()
                self.mft_offset = 0

            sector = self.loader.mft[self.mft_offset:self.mft_offset+SECTOR_SIZE]
            if MFT_ENTRY_MAGIC in sector and current_entry != b'':
                return MFTEntry(current_entry)

            current_entry += sector
            self.mft_offset += SECTOR_SIZE
