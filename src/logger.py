"""
a. For logging the result in log file
"""
import time
import os
import sys

LEVELS = {
    "DEBUG": 3,
    "INFO": 2,
    "WARN": 1,
    "ERROR": 0,
    None: 0,
}
LEVEL = LEVELS[os.environ.get("LOG_LEVEL")]
START_TIME = 0
LOG_FILE = sys.stdout


def fmt_time(delta):
    if delta < 1e-3:
        return f"{round(delta * 1e6, 2)}us"
    if delta < 1:
        return f"{round(delta * 1e3, 2)}ms"
    return f"{round(delta, 2)}s"


def init(file=sys.stdout):
    global START_TIME, LOG_FILE
    START_TIME = time.time()
    LOG_FILE = file


def deinit():
    LOG_FILE.close()


def debug(*args):
    if LEVEL < LEVELS["DEBUG"]:
        return
    print(
        f"[DEBUG][{fmt_time(time.time() - START_TIME)}]",
        *args,
        flush=True,
        file=LOG_FILE
    )


def info(*args):
    if LEVEL < LEVELS["INFO"]:
        return
    print(
        f"[INFO ][{fmt_time(time.time() - START_TIME)}]",
        *args,
        flush=True,
        file=LOG_FILE
    )


def warn(*args):
    if LEVEL < LEVELS["WARN"]:
        return
    print(
        f"[WARN ][{fmt_time(time.time() - START_TIME)}]",
        *args,
        flush=True,
        file=LOG_FILE
    )


def error(*args):
    if LEVEL < LEVELS["ERROR"]:
        return
    print(
        f"[ERROR][{fmt_time(time.time() - START_TIME)}]",
        *args,
        flush=True,
        file=LOG_FILE
    )
