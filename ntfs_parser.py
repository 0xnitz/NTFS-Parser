from ntfs_exception import NTFSException, FileNotFoundException
from mft_iterator import MFTIterator


class NTFSParser:
    def __init__(self, disk):
        try:
            self.mft_iterator = MFTIterator(disk)
            self.disk = disk
        except NTFSException:
            raise FileNotFoundException

    def get_file_contents(self, filename):
        for entry in self.mft_iterator:
            try:
                if entry.is_valid():
                    if filename in entry.get_file_names():
                        return entry.get_data(self.disk,
                                              self.mft_iterator.loader.partition.get_sectors_per_cluster())
            except NTFSException:
                continue
