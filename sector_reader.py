from constants import *


class SectorReader:
    """
    This class deals with input from the physical disks.
    It can read sectors from the disk itself.
    """

    def __init__(self, disk):
        self.disk = disk

    def read_from(self, sector_start, length=1):
        """
        This function reads length sectors from sector_start
        :param sector_start: The sector to start reading from
        :param length: How many sectors to read, default is 1
        :return: Binary data from the sectors
        """

        file = open(self.disk, 'rb')
        file.seek(sector_start * SECTOR_SIZE)
        data = b''

        for i in range(length):
            data += file.read(SECTOR_SIZE)

        return data

    def read_sector(self, sector):
        """
        Reads a single sector
        :param sector: Sector to read
        :return: The sector's binary data
        """

        file = open(self.disk, 'rb')
        file.seek(sector * SECTOR_SIZE)
        return file.read(SECTOR_SIZE)

    def read_until(self, sector_start, string):
        """
        Read sectors until a string
        :param sector_start: The sector to start reading from
        :param string: The string to find
        :return: The Binary data read
        """

        file = open(self.disk, 'rb')
        file.seek(sector_start * SECTOR_SIZE)
        data = b''

        while bytes(string) not in data:
            data += file.read(SECTOR_SIZE)

        return data
