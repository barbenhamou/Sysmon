import psutil
import time
from concurrent.futures import ThreadPoolExecutor

g_partition_lst = set()

def collect_cpu_statistics(interval: float = 1, per_cpu: bool = False) -> list[float]:
    """
    :param interval: The time interval in seconds, over which CPU utilization is calculated.
    :param per_cpu: Whether to calculate CPU utilization entirely or per core.
    :return: A list of CPU utilization percentages values, the length depends on the boolean, and the number of cpu cores.
    """
    lst = []
    if per_cpu:
        lst =  psutil.cpu_percent(interval=interval, percpu=True)
        if not lst:
            # TODO: Add Logger reports on error, failed cpu stats.
            pass

    else:
        stat = psutil.cpu_percent(interval=interval)
        if not stat:
            # TODO: Add Logger reports on error, failed cpu stats.
            pass
        lst.append(stat)

    return lst

def collect_memory_statistics() -> list[int]:
    """
    Collect memory statistics.
    :return: A list of total memory, used memory, available memory, and percentage of used memory.
    """
    mem = psutil.virtual_memory()
    if not mem:
        # TODO: Add Logger reports on error, RAM stats failed.
        pass
    return [mem.used, mem.total, mem.percent]


def collect_disk_statistics() -> list[list[int]]:
    """
    Collect disk statistics, per partition.
    :return: A list of used/total/percent for every partition.
    """
    global g_partition_lst

    partitions_lst = set(psutil.disk_partitions(True))
    if partitions_lst != g_partition_lst:
        symmetric_difference = partitions_lst ^ g_partition_lst
        # TODO: Add Logger reports on error, new partitions.
        pass

    g_partition_lst = partitions_lst

    stats_lst = []
    for partition in partitions_lst:
        partition_stats = psutil.disk_usage(partition.mountpoint)
        if not partition_stats:
            # TODO: Add Logger reports on error, failed partition stats.
            pass
        stats_lst.append([partition_stats.total, partition_stats.used, partition_stats.free, partition_stats.percent])

    return stats_lst

def collect_network_statistics(interval: float) -> list[float]:
    """
    Collecting Network statistics.
    :param interval: The time interval in seconds, over which network statistics are calculated.
    :return: A list with two parameters - upload and download speed.
    """

    net_time_stamp_a =  psutil.net_io_counters()
    if not net_time_stamp_a:
        # TODO: Add Logger reports on error, failed network stats.
        pass

    time.sleep(interval)
    net_time_stamp_b = psutil.net_io_counters()
    if not net_time_stamp_b:
        # TODO: Add Logger reports on error, failed network stats.
        pass

    delta_upload = net_time_stamp_b.bytes_sent - net_time_stamp_a.bytes_sent
    delta_download = net_time_stamp_b.bytes_recv - net_time_stamp_a.bytes_recv

    return [delta_upload / interval, delta_download / interval]

def collect_stats(interval: float) -> dict[str, list]:
    """
    :param interval: The time interval in seconds, over which system's statistics are calculated.
    :return: A dictionary with all the collected statistics.
    """
    with ThreadPoolExecutor(max_workers=5) as ex:
        cpu_stats = ex.submit(collect_cpu_statistics, interval=interval)
        cpu_stats_per_core = ex.submit(collect_cpu_statistics, interval=interval, per_cpu=True)
        mem_stats = ex.submit(collect_memory_statistics)
        disk_stats = ex.submit(collect_disk_statistics)
        net_stats = ex.submit(collect_network_statistics, interval=interval)

    if not (cpu_stats and cpu_stats_per_core and mem_stats and disk_stats and net_stats):
        # TODO: Add Logger reports on error, failed stats.
        pass

    stats_dict = {
        "type": ["stats"],
        "timestamp": [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())],
        "cpu_stats": cpu_stats.result(),
        "cpu_stats_per_core": cpu_stats_per_core.result(),
        "mem_stats": mem_stats.result(),
        "disk_stats": disk_stats.result(),
        "net_stats": net_stats.result()
    }
    return stats_dict

