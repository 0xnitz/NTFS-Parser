from ntfs_exception import NTFSException, FileNotFoundException
from mft_iterator import MFTIterator


class NTFSParser:
    def __init__(self):
        try:
            self.mft_iterator = MFTIterator()
        except NTFSException:
            raise FileNotFoundException

    def get_file_contents(self, filename):
        for entry in self.mft_iterator:
            try:
                if entry.is_valid():
                    if filename in entry.get_file_names():
                        return entry.get_data(
                            self.mft_iterator.loader.drive.locate_largest_partition_sectors_per_cluster(),
                            self.mft_iterator.loader.drive.locate_largest_partition_vbr_offset())
            except NTFSException:
                continue
