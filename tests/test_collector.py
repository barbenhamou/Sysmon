from src.collector import *
import pytest

def sanity_cpu_test():
    assert len(collect_cpu_statistics()) == 1
    assert len(collect_cpu_statistics(per_cpu=True)) >= 1

def sanity_memory_test():
    stats = collect_memory_statistics()
    assert len(stats) == 3
    assert stats[0] <= stats[1]
    assert (stats[0] / stats[1] * 100 - stats[2]) <= 1

def sanity_disk_test():
    lst = collect_disk_statistics()
    for i in lst:
        assert len(i) == 4
        assert i[0] == i[1] + i[2]
        assert abs(i[3] - i[1] / i[0] * 100) <= 1

def sanity_network_test():
    lst = collect_network_statistics()
    assert len(lst) == 2