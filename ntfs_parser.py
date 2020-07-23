from mft import MFT
from file_info import File


class NTFSParser:
    def __init__(self, disk):
        disk = r'\\.\\' + disk + ':'
        self._mft = MFT(disk)
        self._disk = disk

    def get_file_contents(self, filename):
        for entry in self._mft:
            if filename in entry.get_file_names():
                return File(filename, entry.get_data(self._disk,
                                                     self._mft.get_sectors_per_cluster()))
