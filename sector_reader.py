from ntfs_exception import DiskDoesNotExist

# CR: [design] This should be some class constant. Probably Partition
SECTOR_SIZE = 512


class SectorReader:
    # CR: [desing] Should receive only the letter and handle the path
    # manipulation ('C' -> '\\.\C:')
    def __init__(self, disk):
        self.disk = disk
        try:
            self.file = open(self.disk, 'rb')
        except FileNotFoundError:
            # CR: [implementation] Raise an instance not a type
            raise DiskDoesNotExist

    def read_from(self, sector_start, length_in_sectors=1):
        self.file.seek(sector_start * SECTOR_SIZE)
        return self.file.read(SECTOR_SIZE * length_in_sectors)

    # CR: [conventions] Order functions top down
    def read_sector(self, sector):
        return self.read_from(sector)
