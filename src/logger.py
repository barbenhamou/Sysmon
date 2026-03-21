import json
from threading import Lock
import time

g_logger = None

class Logger:
    """
    This class is responsible for logging the data collected by the collector module.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.loq_queue: list[dict] = list()
        self.log_mutex = Lock()
        self.sig = False

    def append_log(self, stats: dict[str, list]):
        """
        This function appends the data collected by the collector module to the log queue.
        :return:
        """
        self.log_mutex.acquire()
        try:
            self.loq_queue.append(stats)
        finally:
            self.log_mutex.release()

    def append_error(self, subsystem, error):
        """
        This function adds appends an error from the collector module to the log queue.
        :return:
        """
        error_log = {
            "type": ["error"],
            "timestamp": [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())],
            "subsystem": subsystem,
            "error description": error
        }

        self.log_mutex.acquire()
        try:
            self.loq_queue.append(error_log)
        finally:
            self.log_mutex.release()

    def write_logs(self):
        """
        This function writes to the log file the data from the run. The log file in json format.
        :return:
        """
        while True:
            if self.loq_queue == list():
                if self.sig:
                    return
                continue

            self.log_mutex.acquire()
            try:
                top_log = self.loq_queue.pop(0)
            finally:
                self.log_mutex.release()

            with open(self.file_path, "a") as f:
                f.write(json.dumps(top_log) + "\n")
