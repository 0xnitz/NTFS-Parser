from sector_reader import SectorReader


class DataRun:
    def __init__(self, disk):
        self.starting_cluster = 0
        self.sectors_per_cluster = 0
        self.cluster_length = 0
        self.sector_reader = SectorReader(r'\\.\\' + disk + ':')

    def read_run(self):
        return self.sector_reader.read_from(
            self.starting_cluster * self.sectors_per_cluster,
            self.cluster_length * self.sectors_per_cluster)
