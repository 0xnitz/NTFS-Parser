from sector_reader import SectorReader, SECTOR_SIZE
from mft_entry import MFTEntry, MFT_ENTRY_SIZE
from partition import Partition


class MFTLoader:
    def __init__(self, disk):
        self.sector_reader = SectorReader(r'\\.\\' + disk + ':')
        self.partition = Partition(disk)
        self.run_index = 0
        self.mft = self.load_mft(disk)

    def load_mft(self, disk):
        mft_entry = self.sector_reader.read_from(self.partition.get_mft_starting_sector(),
                                                 round(MFT_ENTRY_SIZE / SECTOR_SIZE))

        self.mft = MFTEntry(mft_entry).get_data(disk, self.partition.get_sectors_per_cluster(),
                                                read_in_parts=True, run_index=self.run_index)

        self.run_index += 1

        return self.mft
