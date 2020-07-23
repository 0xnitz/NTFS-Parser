from ntfs_exception import NTFSException, FileNotFoundException
from mft_iterator import MFTIterator


class NTFSParser:
    def __init__(self, disk):
        try:
            self.mft_iterator = MFTIterator(disk)
            self.disk = disk
        except NTFSException:
            # CR: [finish] Raise an instance not a class. Also, why even catch
            # if all you do is to raise again?
            raise FileNotFoundException

    # CR: [design] Do you want to return the content or maybe a file?
    def get_file_contents(self, filename):
        for entry in self.mft_iterator:
            # CR: [design] What function throws an exception here? Can it be
            # avoided with checks to make the code cleaner? If not I would
            # probably extract the content to another function for readability
            try:
                if entry.is_valid():
                    if filename in entry.get_file_names():
                        # CR: [design] This statement breaks encapsulation
                        # CR: [design] Can entry be self sufficient? Meaning
                        # can you pass these details in the __init__ so you
                        # could just call entry.get_data()
                        return entry.get_data(self.disk,
                                              self.mft_iterator.loader.partition.get_sectors_per_cluster())
            except NTFSException:
                continue
