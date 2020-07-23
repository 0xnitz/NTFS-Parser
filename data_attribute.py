from ntfs_exception import FileNotFoundException
from attribute import Attribute
from run_list import RunList


class DataAttribute(Attribute):
    DATA_LENGTH_OFFSET = 0x10
    DATA_OFFSET = 0x18

    def __init__(self, attribute_bytes, sectors_per_cluster):
        super().__init__(attribute_bytes)
        self._sectors_per_cluster = sectors_per_cluster

    def get_data(self, disk, read_in_parts=False, run_index=0):
        if self.is_resident():
            length_in_bytes = self._attribute_bytes[DataAttribute.DATA_LENGTH_OFFSET] * 2
            return self._attribute_bytes[DataAttribute.DATA_OFFSET:DataAttribute.DATA_OFFSET + length_in_bytes]

        if read_in_parts:
            run_list = RunList(self._attribute_bytes[self._attribute_bytes[Attribute.RUN_LIST_OFFSET]:],
                               self._sectors_per_cluster, disk)

            if run_index == run_list.get_length():
                raise FileNotFoundException('[] file not found!')

            return run_list.read_run(run_index)

        return super().get_data(disk, self._sectors_per_cluster)
