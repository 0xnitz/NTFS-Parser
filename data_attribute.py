from constants import DATA_LENGTH, DATA_ATTRIBUTE_DATA, RUN_LIST_OFFSET
from ntfs_exception import NTFSException
from attribute import Attribute
from run_list import RunList


class DataAttribute(Attribute):
    def __init__(self, attribute_bytes, sectors_per_cluster, vbr_offset):
        super().__init__(attribute_bytes)
        self.sectors_per_cluster = sectors_per_cluster
        self.vbr_offset = vbr_offset

    def get_data(self):
        if self.is_resident():
            length_in_bytes = self.attribute_bytes[DATA_LENGTH] * 2
            return self.attribute_bytes[DATA_ATTRIBUTE_DATA:DATA_ATTRIBUTE_DATA + length_in_bytes]
        else:
            return RunList(self.attribute_bytes[self.attribute_bytes[RUN_LIST_OFFSET]:],
                           self.sectors_per_cluster, self.vbr_offset).read_all_runs()
