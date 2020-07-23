from ntfs_exception import NTFSException
from sector_reader import SectorReader
from partition import Partition
from mft_entry import MFTEntry

from sys import byteorder


class MFT:
    def __init__(self, disk):
        if byteorder != 'little':
            raise NTFSException('NTFS Parser supports only little endian!')

        self._disk = disk
        self._sector_reader = SectorReader(self._disk)

        partition = Partition(self._disk)
        self.sectors_per_cluster = partition.get_sectors_per_cluster()
        self._mft_starting_sector = partition.get_mft_starting_sector()

        self._mft_chunk_index = 0
        self._mft_chunk = self._read_mft_in_parts(self._disk)

    def __iter__(self):
        self.mft_offset = 0
        return self

    def __next__(self):
        mft_length = len(self._mft_chunk)

        current_entry = b''
        while True:
            if self.mft_offset >= mft_length:
                self._read_mft_in_parts(self._disk)
                self.mft_offset = 0

            sector = self._mft_chunk[self.mft_offset:self.mft_offset + SectorReader.SECTOR_SIZE]
            if MFTEntry.MFT_ENTRY_MAGIC == sector[:0x4] and current_entry != b'':
                next_entry = MFTEntry(current_entry)
                if not next_entry.is_valid():
                    return self.__next__()

                return next_entry

            current_entry += sector
            self.mft_offset += SectorReader.SECTOR_SIZE

    def get_sectors_per_cluster(self):
        return self.sectors_per_cluster

    def _read_mft_in_parts(self, disk):
        mft_entry = self._sector_reader.read_from(self._mft_starting_sector,
                                                  round(MFTEntry.MFT_ENTRY_SIZE / SectorReader.SECTOR_SIZE))

        self._mft_chunk = MFTEntry(mft_entry).get_data(disk, self.get_sectors_per_cluster(),
                                                       read_in_parts=True, run_index=self._mft_chunk_index)

        self._mft_chunk_index += 1
        return self._mft_chunk
