from utils import bytes_to_number
from data_run import DataRun

from typing import List


class RunList:
    def __init__(self, run_list_bytes, sectors_per_cluster, disk):
        self._runs: List[DataRun] = []
        self._parse_runs(run_list_bytes, sectors_per_cluster, disk)

    def read_all_runs(self):
        data = b''
        for run in self._runs:
            data += run.read_run()

        return data

    def read_run(self, run_index=0):
        return self._runs[run_index].read_run()

    def get_length(self):
        return len(self._runs)

    def _parse_runs(self, run_list_bytes, sectors_per_cluster, disk):
        prev_run = None
        i = 0

        while i < len(run_list_bytes):
            size = run_list_bytes[i]
            if size == 0:
                break

            cluster_count_length = size & 0xf
            first_cluster_length = size >> 4

            cluster_count = run_list_bytes[i + 1:i + 1 + cluster_count_length]
            first_cluster = run_list_bytes[
                            i + 1 + cluster_count_length:i + 1 + cluster_count_length + first_cluster_length]

            current_run = DataRun(disk, bytes_to_number(first_cluster),
                                  sectors_per_cluster, bytes_to_number(cluster_count))

            if prev_run is not None:
                current_run.starting_cluster += prev_run.starting_cluster

            i += 1 + cluster_count_length + first_cluster_length

            self._runs.append(current_run)
            prev_run = current_run
