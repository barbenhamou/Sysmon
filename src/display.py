from rich.live import Live
from rich.table import Table
import time
import src.logger as logger
from src.collector import collect_stats

def init_live_display(refresh_per_second: int = 1):
    with Live(refresh_per_second=refresh_per_second) as live:
        while True:
            table = Table(title="System Metrics")
            table.add_column("Metric")
            table.add_column("Stats")
            table.add_column("Units/Description")

            stats, units = collect_stats()

            logger.g_logger.append_log(stats)

            for metric, value in stats.items():
                if metric == "type" or metric == "timestamp":
                    continue
                table.add_row(metric, str(value), units[metric])


            live.update(table)

# init_live_display()