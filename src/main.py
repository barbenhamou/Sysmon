from argparse import ArgumentParser

def main():
    """
    Entry point. CLI parsing and task dispatching
    """
    parser = ArgumentParser()
    parser.add_argument('--interval', help='Polling frequency in seconds.')
    parser.add_argument('--log', help='Specify a log file path.')


if __name__ == '__main__':
    main()