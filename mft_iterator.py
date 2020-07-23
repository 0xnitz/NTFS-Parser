from mft_entry import MFTEntry, MFT_ENTRY_MAGIC
from ntfs_exception import NTFSException
from sector_reader import SECTOR_SIZE
from mft_loader import MFTLoader

from sys import byteorder


class MFTIterator:
    def __init__(self, disk):
        # CR: [design] Is it hard to support big endian?
        if byteorder != 'little':
            # CR: [finish] Raise an instance not a type. Provide information
            raise NTFSException

        self.loader = MFTLoader(disk)
        # CR: [finish] Initialize in __iter__
        self.mft_offset = 0
        self.disk = disk

    def __iter__(self):
        return self

    def __next__(self):
        mft_length = len(self.loader.mft)

        current_entry = b''
        while True:
            if self.mft_offset >= mft_length:
                # CR: [implementation] You are calling load_mft for every
                # iteration + when initializing self.loader
                self.loader.load_mft(self.disk)
                self.mft_offset = 0

            sector = self.loader.mft[self.mft_offset:self.mft_offset+SECTOR_SIZE]
            if MFT_ENTRY_MAGIC in sector and current_entry != b'':
                return MFTEntry(current_entry)

            current_entry += sector
            self.mft_offset += SECTOR_SIZE
