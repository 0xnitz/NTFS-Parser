from constants import *


# CR: [finish] If this can read arbitrary sizes than it's not a SectorReader.
# It is probably a VolumeReader or a DiskReader.
class SectorReader:
    """
    This class deals with input from the physical disks.
    It can read sectors from the disk itself.
    """

    # CR: [finish] What kind of entity is disk? I would first think it is a
    # Disk object or something. In a duck typed language such as python I
    # recommend using more explicit names such as disk_path
    def __init__(self, disk):
        # CR: [implementation] You don't use self.disk anywhere outside
        # __init__, so you can avoid setting it as a property
        self.disk = disk
        self.file = open(self.disk, 'rb')
        # CR: [finish] This name doesn't reflect the data well. What do the
        # values represent?
        self.current_chunk = 0, 0

    # CR: [finish] Rename to length_in_sectors
    def read_from(self, sector_start, length=1):
        """
        This function reads length sectors from sector_start
        :param sector_start: The sector to start reading from
        :param length: How many sectors to read, default is 1
        :return: Binary data from the sectors
        """

        self.file.seek(sector_start * SECTOR_SIZE)

        return self.file.read(SECTOR_SIZE * length)

    # CR: [design] Avoid code duplication by using self.read_from()
    def read_sector(self, sector):
        """
        Reads a single sector
        :param sector: Sector to read
        :return: The sector's binary data
        """

        self.file.seek(sector * SECTOR_SIZE)
        return self.file.read(SECTOR_SIZE)

    # CR: [design] Let's talk about these functions. I had a hard time
    # understanding them.
    def read_until(self, sector_start, byte_string):
        """
        Read sectors until a byte-string is found. The functions reads from the disk in chunks to minimize runtime.
        :param sector_start: The sector to start reading from
        :param byte_string: The byte_string to find
        :return: The Binary data read
        """

        # Checking if a new chunk needs to be generated
        self.read_new_chunk(sector_start)

        sectors_read = 0
        data = b''

        # Iterating over the chunk's sectors and checking if the byte-string is found in them,
        # then returning up to the byte-string
        for i in range(sector_start - self.current_chunk[0], CHUNK_SIZE):
            # Calculating the current sector in the chunk
            current_sector = self.current_chunk[1][i * SECTOR_SIZE:i * SECTOR_SIZE + SECTOR_SIZE]

            # Checking if the byte-string is in the current sector and it's not the first sector read
            # Example: FILE temp temp temp FILE
            # We start reading at the FILE string,
            # we want to read up to the next FILE and not stop on the first occurrence
            if byte_string in current_sector and i != sector_start - self.current_chunk[0]:
                break
            else:
                # Incrementing the amount of sectors read and adding the current sector to the total data read
                sectors_read += 1
                data += current_sector

        return data, sectors_read

    def read_new_chunk(self, sector_from):
        """
        This function reads from the disk in chunks.
        It checks if a new chunks needs to be generated and generates it.
        :param sector_from: Is the sector id the program wants to read from
        :return:
        """

        # Checking if our offset is not in the the current saved chunk to check if a new chunk should be generated
        if sector_from < self.current_chunk[0] or sector_from >= self.current_chunk[0] + CHUNK_SIZE:
            # Checking if the sector_from will be included in the next chunk, if so read the adjacent next chunk
            # Otherwise, generate a new chunk from sector_from
            if self.current_chunk[0] + CHUNK_SIZE < sector_from < self.current_chunk[0] + CHUNK_SIZE * 2:
                sector_list = self.read_from(self.current_chunk[0] + CHUNK_SIZE, CHUNK_SIZE)
                self.current_chunk = self.current_chunk[0] + CHUNK_SIZE, sector_list
            else:
                sector_list = self.read_from(sector_from, CHUNK_SIZE)
                self.current_chunk = sector_from, sector_list
