from partition import Partition, OEM_ID

from operator import attrgetter
from typing import List
from os import popen
from re import match


class PhysicalDrive:
    def __init__(self, drive_number):
        self.partitions: List[Partition] = []
        self.drive_number = drive_number
        self._get_partitions()

    def locate_largest_partition_vbr_offset(self):
        return self._get_largest_partition().get_vbr_offset()

    def locate_largest_partition_mft_starting_sector(self):
        return self._get_largest_partition().get_mft_starting_sector()

    def locate_largest_partition_sectors_per_cluster(self):
        return self._get_largest_partition().get_sectors_per_cluster()

    def _get_largest_partition(self):
        return max(self.partitions, key=attrgetter('size'))

    def _get_partitions(self):
        partitions = popen('wmic partition get StartingOffset, DiskIndex').read().split('\n')
        partitions = [i.split() for i in partitions if match(r'.*\d+.*', i)]

        for partition in partitions:
            if str(self.drive_number) != partition[0]:
                continue

            starting_offset = int(partition[1])
            current_partition = Partition(starting_offset, self.drive_number)

            if OEM_ID in current_partition.get_oem_id():
                self.partitions.append(current_partition)
