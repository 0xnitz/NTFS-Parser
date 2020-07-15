class NTFSHandler:
    def __init__(self, sector_reader):
        """
        A constructor for the NTFSHandler class
        :param sector_reader: a SectorReader object
        """

        self.sectors_per_cluster = 0
        self.mft_entry_size = 0
        self.sector_reader = sector_reader

    def find_mft(self):
        """
        This function reads the boot sector of the file system and locates the start of the MFT
        :return: the starting sector for the MFT
        """

        return 0
