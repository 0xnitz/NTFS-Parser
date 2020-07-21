from ntfs_exception import NTFSException, ReadEntireMFTException, FileNotFoundException
from mft_iterator import MFTIterator


class NTFSParser:
    def __init__(self):
        self.mft_iterator = MFTIterator()

    def find_file(self, filename):
        try:
            for i, entry in enumerate(self.mft_iterator):
                if entry.is_valid():
                    try:
                        if entry.get_filename() == filename:
                            return entry.get_data(
                                self.mft_iterator.loader.drive.locate_largest_partition_sectors_per_cluster(),
                                self.mft_iterator.loader.drive.locate_largest_partition_vbr_offset())
                    except NTFSException:
                        continue
        except ReadEntireMFTException:
            raise FileNotFoundException
