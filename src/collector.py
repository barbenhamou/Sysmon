import psutil
import time

def collect_cpu_statistics(interval: float = 1, per_cpu: bool = False) -> list[float]:
    """
    :param interval: The time interval in seconds, over which CPU utilization is calculated.
    :param per_cpu: Whether to calculate CPU utilization entirely or per core.
    :return: A list of CPU utilization percentages values, the length depends on the boolean, and the number of cpu cores.
    """
    lst = []
    if per_cpu:
        lst =  psutil.cpu_percent(interval=interval, percpu=True)
    else:
        lst.append(psutil.cpu_percent(interval=interval))

    return lst

def collect_memory_statistics() -> list[int]:
    """
    Collect memory statistics.
    :return: A list of total memory, used memory, available memory, and percentage of used memory.
    """
    mem = psutil.virtual_memory()
    return [mem.used, mem.total, mem.percent]


def collect_disk_statistics() -> list[list[int]]:
    """
    Collect disk statistics, per partition.
    :return: A list of used/total/percent for every partition.
    """

    partitions_lst = psutil.disk_partitions(True)
    stats_lst = []
    for partition in partitions_lst:
        partition_stats = psutil.disk_usage(partition.mountpoint)
        stats_lst.append([partition_stats.total, partition_stats.used, partition_stats.free, partition_stats.percent])

    return stats_lst

def collect_network_statistics(interval: float) -> list[float]:
    """
    Collecting Network statistics.
    :param interval: The time interval in seconds, over which network statistics are calculated.
    :return: A list with two parameters - upload and download speed.
    """

    net_time_stamp_a =  psutil.net_io_counters()
    time.sleep(interval)
    net_time_stamp_b = psutil.net_io_counters()

    delta_upload = net_time_stamp_b.bytes_sent - net_time_stamp_a.bytes_sent
    delta_download = net_time_stamp_b.bytes_recv - net_time_stamp_a.bytes_recv

    return [delta_upload / interval, delta_download / interval]
