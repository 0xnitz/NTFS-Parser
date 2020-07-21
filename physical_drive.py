from operator import attrgetter
from typing import List
from os import popen

from partition import Partition
from constants import OEM_ID


class PhysicalDrive:
    def __init__(self, drive_number):
        self.partitions: List[Partition] = []
        self.drive_number = drive_number

    def locate_largest_partition_vbr_offset(self):
        self._get_partitions()
        return self._get_largest_partition().get_vbr_offset()

    def locate_largest_partition_mft_starting_sector(self):
        self._get_partitions()
        return self._get_largest_partition().get_mft_starting_sector()

    def locate_largest_partition_sectors_per_cluster(self):
        self._get_partitions()
        return self._get_largest_partition().get_sectors_per_cluster()

    def _get_largest_partition(self):
        return max(self.partitions, key=attrgetter('size'))

    def _get_partitions(self):
        partitions = popen('wmic partition get StartingOffset, Name').read().split('\n')
        partitions = [i.split() for i in partitions if 'Disk' in i]

        for partition in partitions:
            if str(self.drive_number) not in partition[1]:
                continue

            starting_offset = int(partition[4])
            name = partition[1]
            current_partition = Partition(name, starting_offset)

            if OEM_ID in current_partition.get_oem_id():
                self.partitions.append(current_partition)
