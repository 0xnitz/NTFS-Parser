from constants import *


class SectorReader:
    """
    This class deals with input from the physical disks.
    It can read sectors from the disk itself.
    """

    def __init__(self, disk):
        self.disk = disk
        self.file = open(self.disk, 'rb')

    def read_from(self, sector_start, length=1):
        """
        This function reads length sectors from sector_start
        :param sector_start: The sector to start reading from
        :param length: How many sectors to read, default is 1
        :return: Binary data from the sectors
        """

        self.file.seek(sector_start * SECTOR_SIZE)
        data = b''

        for i in range(length):
            data += self.file.read(SECTOR_SIZE)

        return data

    def read_sector(self, sector):
        """
        Reads a single sector
        :param sector: Sector to read
        :return: The sector's binary data
        """

        self.file.seek(sector * SECTOR_SIZE)
        return self.file.read(SECTOR_SIZE)

    def read_until(self, sector_start, byte_string):
        """
        Read sectors until a string
        :param sector_start: The sector to start reading from
        :param byte_string: The byte_string to find
        :return: The Binary data read
        """

        self.file.seek(sector_start * SECTOR_SIZE)
        sectors_read = 1
        data = self.file.read(SECTOR_SIZE)
        sector = b''

        while byte_string not in sector:
            data += sector
            sector = self.file.read(SECTOR_SIZE)
            sectors_read += 1

        return data, sectors_read
