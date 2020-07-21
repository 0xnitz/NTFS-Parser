from constants import SECTOR_SIZE, MFT_ENTRY_MAGIC
from ntfs_exception import ReadEntireMFTException
from mft_loader import MFTLoader
from mft_entry import MFTEntry


class MFTIterator:
    def __init__(self):
        self.loader = MFTLoader()
        self.mft_offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        mft_length = len(self.loader.mft)

        current_entry = b''
        while True:
            if self.mft_offset >= mft_length:
                raise ReadEntireMFTException

            sector = self.loader.mft[self.mft_offset:self.mft_offset+SECTOR_SIZE]
            if MFT_ENTRY_MAGIC in sector and current_entry != b'':
                return MFTEntry(current_entry)

            current_entry += sector
            self.mft_offset += SECTOR_SIZE
