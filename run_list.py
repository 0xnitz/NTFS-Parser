from utils import bytes_to_number
from data_run import DataRun
from typing import List


class RunList:
    def __init__(self, run_list_bytes, sectors_per_cluster, vbr_offset):
        self.runs: List[DataRun] = []

        prev_run = 0
        i = 0

        # Iterate over the run-list
        while i < len(run_list_bytes):
            current_run = DataRun(vbr_offset)

            size = run_list_bytes[i]
            if size == 0:
                break

            # The size is one byte,
            # and it's nibbles represent the amount of bytes the first_cluster and the cluster_length will take
            cluster_count_length = size & 0xf
            first_cluster_length = size >> 4

            # Extracting the cluster_count and first_cluster
            cluster_count = run_list_bytes[i + 1:i + 1 + cluster_count_length]
            first_cluster = run_list_bytes[
                            i + 1 + cluster_count_length:i + 1 + cluster_count_length + first_cluster_length]

            current_run.starting_cluster = bytes_to_number(first_cluster)
            current_run.cluster_length = bytes_to_number(cluster_count)
            current_run.sectors_per_cluster = sectors_per_cluster

            if prev_run != 0:
                current_run.starting_cluster += prev_run.starting_cluster

            # Jumping to the next cluster run
            i += 1 + cluster_count_length + first_cluster_length

            self.runs.append(current_run)
            prev_run = current_run

    def read_all_runs(self):
        data = b''
        for run in self.runs:
            data += run.read_run()

        return data

    def sector_in_run(self, sector):
        return any([run.sector_in_run(sector) for run in self.runs])
