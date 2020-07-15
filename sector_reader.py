SECTOR_SIZE = 512


class SectorReader:
    def __init__(self, disk):
        self.disk = disk

    def read_from(self, sector_start, length=1):
        file = open(self.disk, 'rb')
        file.seek(sector_start * SECTOR_SIZE)
        return file.read(SECTOR_SIZE * length)

    def read_sector(self, sector):
        file = open(self.disk, 'rb')
        file.seek(sector * SECTOR_SIZE)
        return file.read(SECTOR_SIZE)

    def read_until(self, sector_start, string):
        file = open(self.disk, 'rb')
        file.seek(sector_start * SECTOR_SIZE)
        data = b''

        while bytes(string) not in data:
            data += file.read(SECTOR_SIZE)

        return data
