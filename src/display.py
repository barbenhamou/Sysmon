from rich.live import Live
from rich.console import Console
from rich.table import Table

class Display:
    def __init__(self, refresh_rate: int = 1):
        self.refresh_rate = refresh_rate


from rich.live import Live
from rich.table import Table
import time
from src.collector import collect_stats

with Live(refresh_per_second=1) as live:
    while True:
        table = Table(title="System Metrics")
        table.add_column("Metric")
        table.add_column("Stats")
        table.add_column("Units/Description")

        stats, units = collect_stats()
        for metric, value in stats.items():
            if metric == "type" or metric == "timestamp":
                continue
            table.add_row(metric, str(value), units[metric])


        live.update(table)
        time.sleep(2)