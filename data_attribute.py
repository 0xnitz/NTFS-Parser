from ntfs_exception import FileNotFoundException
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
        self.run_index = -1

    def get_data(self, read_in_parts=False, run_index=0):
        if self.is_resident():
            length_in_bytes = self.attribute_bytes[DATA_LENGTH_OFFSET] * 2
            return self.attribute_bytes[DATA_OFFSET:DATA_OFFSET + length_in_bytes]

        if read_in_parts:
            run_list = RunList(self.attribute_bytes[self.attribute_bytes[RUN_LIST_OFFSET]:],
                                             self.sectors_per_cluster, self.vbr_offset)

            if run_index == run_list.get_length():
                raise FileNotFoundException

            return run_list.read_run(run_index)

        return RunList(self.attribute_bytes[self.attribute_bytes[RUN_LIST_OFFSET]:],
                       self.sectors_per_cluster, self.vbr_offset).read_all_runs()
