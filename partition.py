from sector_reader import SectorReader
from utils import bytes_to_number

OEM_ID = b'NTFS'
OEM_ID_OFFSET = 0x3
MFT_START_SECTOR_OFFSET = 0x30
SECTORS_PER_CLUSTER_OFFSET = 0xd
PARTITION_SIZE_OFFSET = 0x28


class Partition:
    def __init__(self, disk):
        self.size = 0
        self.mft_starting_sector = 0
        self.sectors_per_cluster = 0
        self.oem_id = b''

        self._read_boot_sector(disk)

    def get_mft_starting_sector(self):
        return self.mft_starting_sector

    def get_sectors_per_cluster(self):
        return self.sectors_per_cluster

    def get_oem_id(self):
        return self.oem_id

    def _read_boot_sector(self, disk):
        boot_sector = SectorReader(r'\\.\\' + disk + ':').read_sector(0)

        self.oem_id = boot_sector[OEM_ID_OFFSET:OEM_ID_OFFSET+8]
        self.sectors_per_cluster = boot_sector[SECTORS_PER_CLUSTER_OFFSET]
        self.mft_starting_sector = bytes_to_number(boot_sector[MFT_START_SECTOR_OFFSET:MFT_START_SECTOR_OFFSET+8])\
                                   * self.sectors_per_cluster
        self.size = bytes_to_number(boot_sector[PARTITION_SIZE_OFFSET:PARTITION_SIZE_OFFSET+8])
