from src.collector import *
import src.collector as collector
from types import SimpleNamespace
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
    assert lst[0] >= 0
    assert lst[1] >= 0

def test_collect_cpu_statistics(monkeypatch: pytest.MonkeyPatch):
    def dummy(interval = 1, percpu = False):
        return 0

    monkeypatch.setattr(collector.psutil, "cpu_percent", dummy)

    stats = collect_cpu_statistics()
    assert stats == [-1]

def test_collect_cpu_statistics_per_cpu(monkeypatch: pytest.MonkeyPatch):
    def dummy(interval = 1, percpu = False):
        return None

    monkeypatch.setattr(collector.psutil, "cpu_percent", dummy)

    stats = collect_cpu_statistics(per_cpu=True)
    assert stats == [-1]

def test_collect_mem(monkeypatch: pytest.MonkeyPatch):
    def dummy():
        return None

    monkeypatch.setattr(collector.psutil, "virtual_memory", dummy)

    stats = collect_memory_statistics()
    assert stats == [-1]


def test_collect_disk(monkeypatch: pytest.MonkeyPatch):
    def dummy(bol: bool = False):
        return None

    monkeypatch.setattr(collector.psutil, "disk_partitions", dummy)

    stats = collect_disk_statistics()
    assert stats == [-1]

def test_collect_network(monkeypatch: pytest.MonkeyPatch):
    def dummy():
        return None

    monkeypatch.setattr(collector.psutil, "net_io_counters", dummy)

    stats = collect_network_statistics()
    assert stats == [-1]

def test_collect_disk_statistics_depth(monkeypatch):
    bar = SimpleNamespace(mountpoint="/bar")
    foo = SimpleNamespace(mountpoint="/foo")

    monkeypatch.setattr(collector.psutil, "disk_partitions", lambda all=True: [bar, foo])

    def fake_disk_usage(mountpoint):
        if mountpoint == "/bar":
            return SimpleNamespace(total=100, used=40, free=60, percent=40)
        return None

    monkeypatch.setattr(collector.psutil, "disk_usage", fake_disk_usage)

    stats = collector.collect_disk_statistics()
    assert stats == [[100, 40, 60, 40]]


def test_collect_network_statistics_depth(monkeypatch):
    timestamps = [
        SimpleNamespace(bytes_sent=4000, bytes_recv=6500),
        SimpleNamespace(bytes_sent=5000, bytes_recv=7000),
    ]

    def fake_net_io_counters():
        return timestamps.pop(0)

    def fake_sleep():
        return None

    monkeypatch.setattr(collector.psutil, "net_io_counters", fake_net_io_counters)
    monkeypatch.setattr(collector.time, "sleep", fake_sleep)

    stats = collector.collect_network_statistics()
    assert stats == [1000, 500]
