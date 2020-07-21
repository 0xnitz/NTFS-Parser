from sector_reader import SectorReader
from constants import VBR_OFFSET


class DataRun:
    def __init__(self, vbr_offset):
        self.starting_cluster = 0
        self.sectors_per_cluster = 0
        self.cluster_length = 0
        self.vbr_offset = vbr_offset
        self.sector_reader = SectorReader(r'\\.\physicaldrive0')

    def read_run(self):
        return self.sector_reader.read_from(
            self.starting_cluster * self.sectors_per_cluster + self.vbr_offset, self.cluster_length)

    def sector_in_run(self, sector):
        return self.starting_cluster * self.sectors_per_cluster <= sector <\
               (self.starting_cluster + self.cluster_length) * self.sectors_per_cluster
