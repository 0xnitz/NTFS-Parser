from ntfs_exception import DiskDoesNotExist


class SectorReader:
    SECTOR_SIZE = 512

    def __init__(self, disk):
        self._disk = disk
        try:
            self.file = open(self._disk, 'rb')
        except FileNotFoundError:
            raise DiskDoesNotExist(f'[] ERROR! Disk {disk} does not exist!')

    def read_sector(self, sector):
        return self.read_from(sector)

    def read_from(self, sector_start, length_in_sectors=1):
        self.file.seek(sector_start * SectorReader.SECTOR_SIZE)
        return self.file.read(SectorReader.SECTOR_SIZE * length_in_sectors)
