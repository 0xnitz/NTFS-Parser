from sector_reader import SectorReader
from utils import bytes_to_number
from constants import SECTOR_SIZE


class Partition:
    def __init__(self, name, starting_offset):
        self.name = name
        self.starting_offset = starting_offset

        self.size = 0
        self.mft_starting_sector = 0
        self.sectors_per_cluster = 0
        self.oem_id = b''

        self._read_boot_sector()

    def get_size(self):
        return self.size

    def get_mft_starting_sector(self):
        return self.mft_starting_sector

    def get_sectors_per_cluster(self):
        return self.sectors_per_cluster

    def get_vbr_offset(self):
        return round(self.starting_offset / SECTOR_SIZE)

    def get_oem_id(self):
        return self.oem_id

    def _read_boot_sector(self):
        vbr_offset = self.get_vbr_offset()
        boot_sector = SectorReader(r'\\.\physicaldrive0').read_sector(vbr_offset)

        self.oem_id = boot_sector[0x3:0xb]
        self.sectors_per_cluster = boot_sector[0xd]
        self.mft_starting_sector = bytes_to_number(boot_sector[0x30:0x38]) * self.sectors_per_cluster
        self.size = bytes_to_number(boot_sector[0x28:0x30])
