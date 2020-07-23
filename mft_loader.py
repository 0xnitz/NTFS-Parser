from sector_reader import SectorReader, SECTOR_SIZE
from mft_entry import MFTEntry, MFT_ENTRY_SIZE
from partition import Partition


# CR: [design] I'm not sure if there's a clear benefiet in having this class as
# a seperate entity. You could make load_mft a private function in MftIterator
# (and just call that class Mft)
class MFTLoader:
    def __init__(self, disk):
        # CR: [bug?] You have an extra slash
        self.sector_reader = SectorReader(r'\\.\\' + disk + ':')
        # CR: [design] Is partition part of the Mft, or the other way around?
        self.partition = Partition(disk)
        # CR: [design] This doesn't belong in this level of abstraction. It's
        # also not really used.
        self.run_index = 0
        # CR: [design] Why call load_mft from init?
        self.mft = self.load_mft(disk)

    def load_mft(self, disk):
        mft_entry = self.sector_reader.read_from(self.partition.get_mft_starting_sector(),
                                                 round(MFT_ENTRY_SIZE / SECTOR_SIZE))

        self.mft = MFTEntry(mft_entry).get_data(disk, self.partition.get_sectors_per_cluster(),
                                                read_in_parts=True, run_index=self.run_index)

        self.run_index += 1
        return self.mft
