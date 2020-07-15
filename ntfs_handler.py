from sector_reader import SectorReader, SECTOR_SIZE


class NTFSHandler:
    def __init__(self):
        """
        A constructor for the NTFSHandler class
        :param sector_reader: a SectorReader object
        """

        self.sectors_per_cluster = 0
        self.mft_entry_size = 0
        self.mft_start_sector = 0
        self.sector_reader = SectorReader(r'\\.\physicaldisk0')
        self.MFT_OFFSET = 0
        self.entry_i = 0

    def find_mft(self):
        """
        This function reads the boot sector of the file system and locates the start of the MFT
        :return: the starting sector for the MFT
        """
        self.MFT_OFFSET = 1
        self.mft_entry_size = 0x200 # Change this to size in sectors
        self.sectors_per_cluster = 8
        return self.MFT_OFFSET

    def get_next_entry(self):
        """
        This function reads the next mft entry and returns it
        :return: bytes object of an mft entry
        """
        # MFT file not yet found
        if self.MFT_OFFSET == 0:
            return

        # Finished reading the MFT
        if self.mft_entry_size * SECTOR_SIZE == self.entry_i * SECTOR_SIZE:
            return READ_ENTIRE_MFT

        temp_file = open('sample_mft.bin', 'rb')
        temp_file.seek(self.entry_i * self.mft_entry_size)

        self.entry_i += 1
        return temp_file.read(self.mft_entry_size)

    def get_entry_size(self):
        return self.mft_entry_size
