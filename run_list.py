from utils import bytes_to_number
from data_run import DataRun
from typing import List


class RunList:
    def __init__(self, run_list_bytes, sectors_per_cluster, vbr_offset):
        self.runs: List[DataRun] = []
        self._parse_runs(run_list_bytes, sectors_per_cluster, vbr_offset)

    def read_all_runs(self):
        data = b''
        for run in self.runs:
            data += run.read_run()

        return data

    def _parse_runs(self, run_list_bytes, sectors_per_cluster, vbr_offset):
        prev_run = 0
        i = 0

        while i < len(run_list_bytes):
            current_run = DataRun(vbr_offset)

            size = run_list_bytes[i]
            if size == 0:
                break

            cluster_count_length = size & 0xf
            first_cluster_length = size >> 4

            cluster_count = run_list_bytes[i + 1:i + 1 + cluster_count_length]
            first_cluster = run_list_bytes[
                            i + 1 + cluster_count_length:i + 1 + cluster_count_length + first_cluster_length]

            current_run.starting_cluster = bytes_to_number(first_cluster)
            current_run.cluster_length = bytes_to_number(cluster_count)
            current_run.sectors_per_cluster = sectors_per_cluster

            if prev_run != 0:
                current_run.starting_cluster += prev_run.starting_cluster

            i += 1 + cluster_count_length + first_cluster_length

            self.runs.append(current_run)
            prev_run = current_run
