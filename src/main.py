import threading
from argparse import ArgumentParser
from pathlib import Path
import logger
import signal
import time
import display

stop = threading.Event()

def signal_handler(sig, frame):
    logger.g_logger.append_log({"type": ["exit"], "timestamp": [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]})
    stop.set()
    # logger.g_logger.sig = True
    # logger.g_logger.write_logs()
    print("Ctrl+C pressed. Exiting...")
    exit(0)

def main():
    """
    Entry point. CLI parsing and task dispatching
    """
    parser = ArgumentParser()
    parser.add_argument('--interval', help='Polling frequency in seconds.')
    parser.add_argument('--log', help='Specify a log file path.')

    args = parser.parse_args()

    log_file = Path(str(args.log)) if args.log and str(args.log).endswith(".json") else Path("log.json")
    interval = float(args.interval) if args.interval else 1

    if not log_file.exists():
        log_file.touch()

    if interval <= 0:
        print("Polling frequency must be >0. O.w it's a math crime!!")
        return

    logger.g_logger = logger.Logger(str(log_file))

    t = threading.Thread(target=logger.g_logger.write_logs, args=(stop,))
    t.start()

    signal.signal(signal.SIGINT, signal_handler)
    display.init_live_display(refresh_per_second=interval)

    t.join()

if __name__ == '__main__':
    main()