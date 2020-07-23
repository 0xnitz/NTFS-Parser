from sector_reader import SectorReader
from utils import bytes_to_number


class Partition:
    OEM_ID = b'NTFS'
    OEM_ID_OFFSET = 0x3
    MFT_START_SECTOR_OFFSET = 0x30
    SECTORS_PER_CLUSTER_OFFSET = 0xd
    PARTITION_SIZE_OFFSET = 0x28

    def __init__(self, disk):
        self.mft_starting_sector = 0
        self.sectors_per_cluster = 0

        self._read_boot_sector(disk)

    def get_mft_starting_sector(self):
        return self.mft_starting_sector

    def get_sectors_per_cluster(self):
        return self.sectors_per_cluster

    def _read_boot_sector(self, disk):
        boot_sector = SectorReader(disk).read_sector(0)

        self.sectors_per_cluster = boot_sector[Partition.SECTORS_PER_CLUSTER_OFFSET]
        self.mft_starting_sector = bytes_to_number(boot_sector[Partition.MFT_START_SECTOR_OFFSET:
                                                               Partition.MFT_START_SECTOR_OFFSET+8])\
                                   * self.sectors_per_cluster
