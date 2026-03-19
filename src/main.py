from argparse import ArgumentParser
from pathlib import Path

def main():
    """
    Entry point. CLI parsing and task dispatching
    """
    parser = ArgumentParser()
    parser.add_argument('--interval', help='Polling frequency in seconds.')
    parser.add_argument('--log', help='Specify a log file path.')

    args = parser.parse_args()

    log_file = Path(str(args.log)) if args.log and str(args.log).endswith(".json") else "C:\\temp\\log.json"
    interval = float(args.interval) if args.interval else 1

    if not log_file.exists():
        log_file.touch()

    if interval <= 0:
        print("Polling frequency must be >0. O.w it's a math crime!!")
        return

if __name__ == '__main__':
    main()