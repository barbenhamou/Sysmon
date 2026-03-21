import json

class Logger:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.stats = dict()
        self.errors = list()

    def append_log(self):
        """
        This function writes to the log file the data from the previous run. The log file in json format.
        Flushes error and stats at the end.
        :return:
        """
        pass

    def add_error(self):
        """
        This function adds an error to the list of errors. Will be added as a label in the json.
        :return:
        """
        pass

    def update_stats(self):
        """
        Updates the stats from the collector's results.
        :return:
        """
        pass