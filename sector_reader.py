from constants import *


class SectorReader:
    """
    This class deals with input from the physical disks.
    It can read sectors from the disk itself.
    """

    def __init__(self, disk):
        self.disk = disk
        self.current_chunk = {0: 0}
        self.file = open(self.disk, 'rb')

    def read_from(self, sector_start, length=1):
        """
        This function reads length sectors from sector_start
        :param sector_start: The sector to start reading from
        :param length: How many sectors to read, default is 1
        :return: Binary data from the sectors
        """

        self.file.seek(sector_start * SECTOR_SIZE)

        return self.file.read(SECTOR_SIZE * length)

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

        self.read_new_chunk(sector_start)

        sectors_read = 0
        data = b''

        # Move get new chunk to a function and do a recursive call if bytestring was not read
        # Change all function to use chunks
        for i in range(sector_start - list(self.current_chunk.keys())[0], CHUNK_SIZE):
            current_sector = list(self.current_chunk.values())[0][i * SECTOR_SIZE:i * SECTOR_SIZE + SECTOR_SIZE]
            if byte_string in current_sector and i != sector_start - list(self.current_chunk.keys())[0]:
                break
            else:
                sectors_read += 1
                data += current_sector
        else:
            pass
            #recursive_ret = self.read_until(list(self.current_chunk.keys())[0] + 1, byte_string)
            #data += recursive_ret[0]
            #sectors_read += recursive_ret[1]

        return data, sectors_read

    def read_new_chunk(self, sector_from):
        if sector_from < list(self.current_chunk.keys())[0] or \
                sector_from >= list(self.current_chunk.keys())[0] + CHUNK_SIZE:
            if list(self.current_chunk.keys())[0] == 0:
                sector_list = self.read_from(sector_from, CHUNK_SIZE)
                self.current_chunk = {sector_from: sector_list}
            else:
                sector_list = self.read_from(list(self.current_chunk.keys())[-1] + CHUNK_SIZE, CHUNK_SIZE)
                self.current_chunk = {list(self.current_chunk.keys())[-1] + CHUNK_SIZE: sector_list}
