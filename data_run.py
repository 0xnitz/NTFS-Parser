from sector_reader import SectorReader


class DataRun:
    def __init__(self, disk, starting_cluster, sectors_per_cluster, cluster_length):
        self.starting_cluster = starting_cluster
        self._sectors_per_cluster = sectors_per_cluster
        self._cluster_length = cluster_length
        self._sector_reader = SectorReader(disk)

    def read_run(self):
        return self._sector_reader.read_from(
            self.starting_cluster * self._sectors_per_cluster,
            self._cluster_length * self._sectors_per_cluster)
