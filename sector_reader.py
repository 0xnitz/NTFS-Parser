SECTOR_SIZE = 512


class SectorReader:
    def __init__(self, disk):
        self.disk = disk
        self.file = open(self.disk, 'rb')

    def read_from(self, sector_start, length_in_sectors=1):
        self.file.seek(sector_start * SECTOR_SIZE)
        return self.file.read(SECTOR_SIZE * length_in_sectors)

    def read_sector(self, sector):
        return self.read_from(sector)
