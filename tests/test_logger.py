import json
import threading
import time
from pathlib import Path
import pytest
from src.logger import Logger


def sanity_log_queue():
    logger = Logger("dummy.json")
    stats = {
        "type": ["stats"],
        "timestamp": ["2026-03-25 12:00:00"],
        "cpu": [55.2],
    }

    logger.append_log(stats)

    assert len(logger.loq_queue) == 1
    assert logger.loq_queue[0] == stats


def test_error_appending(monkeypatch: pytest.MonkeyPatch):
    logger = Logger("dummy.json")

    monkeypatch.setattr(time, "strftime", lambda fmt, t: "2026-03-26 12:34:56")

    logger.append_error("cpu", "read failed")

    assert len(logger.loq_queue) == 1
    assert logger.loq_queue[0] == {
        "type": ["error"],
        "timestamp": ["2026-03-26 12:34:56"],
        "subsystem": "cpu",
        "error description": "read failed",
    }


def test_written_data():
    logger = Logger("dummy.json")

    logger.append_log({
        "type": ["stats"],
        "timestamp": ["2026-03-26 12:00:00"],
        "cpu": [10.5],
    })

    stop = threading.Event()
    stop.set()

    logger.write_logs(stop)

    lines = Path("dummy.json").read_text().splitlines()
    assert len(lines) == 1

    written = json.loads(lines[0])
    assert written == {
        "type": ["stats"],
        "timestamp": ["2026-03-26 12:00:00"],
        "cpu": [10.5],
    }

def test_stop_event():
    logger = Logger("dummy.json")

    stop = threading.Event()
    stop.set()

    logger.write_logs(stop)

    assert not Path("dummy.json").exists() or Path("dummy.json").read_text() == ""