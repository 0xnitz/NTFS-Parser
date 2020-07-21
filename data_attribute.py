from attribute import Attribute
from run_list import RunList

DATA_LENGTH_OFFSET = 0x10
DATA_OFFSET = 0x18
RUN_LIST_OFFSET = 0x20


class DataAttribute(Attribute):
    def __init__(self, attribute_bytes, sectors_per_cluster, vbr_offset):
        super().__init__(attribute_bytes)
        self.sectors_per_cluster = sectors_per_cluster
        self.vbr_offset = vbr_offset

    def get_data(self):
        if self.is_resident():
            length_in_bytes = self.attribute_bytes[DATA_LENGTH_OFFSET] * 2
            return self.attribute_bytes[DATA_OFFSET:DATA_OFFSET + length_in_bytes]
        else:
            return RunList(self.attribute_bytes[self.attribute_bytes[RUN_LIST_OFFSET]:],
                           self.sectors_per_cluster, self.vbr_offset).read_all_runs()
