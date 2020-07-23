from run_list import RunList


class Attribute:
    RUN_LIST_OFFSET = 0x20
    ATTRIBUTE_NON_RESIDENT_FLAG_OFFSET = 0x8

    def __init__(self, attribute_bytes):
        self._attribute_bytes = attribute_bytes

    def is_resident(self):
        return not self._attribute_bytes[Attribute.ATTRIBUTE_NON_RESIDENT_FLAG_OFFSET]

    def get_data(self, disk, sectors_per_cluster):
        if self.is_resident():
            pass
        else:
            return RunList(self._attribute_bytes[self._attribute_bytes[Attribute.RUN_LIST_OFFSET]:],
                           sectors_per_cluster, disk).read_all_runs()
