import datetime
import threading as th
from enum import Enum, auto
from typing import Any, Callable, Optional


class LogLevel(Enum):
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    VERBOSE = auto()


class LogPosition(Enum):
    HEAD = auto()
    BOTTOM = auto()
    BURGER = auto()


def _log(
    level: LogLevel = LogLevel.INFO,
    pos: LogPosition = LogPosition.BURGER,
    timestamp: bool = True,
    elapsed_time: bool = False,
    fname: bool = False,
    tid: bool = False,
    inputval: bool = False,
    inputval_func: Optional[Callable] = None,
    retval: bool = False,
    retval_func: Optional[Callable] = None,
    top_word: str = "",
    bottom_word: str = "",
) -> Callable:
    def _inner(f: Callable) -> Callable:
        def _wrapper(*args: Any, **keywords: dict[str, Any]) -> Any:
            time_s = datetime.datetime.now()
            if pos != LogPosition.BOTTOM:
                log_s = f"[{level.name}]"
                if timestamp:
                    log_s = log_s + f" {time_s}"
                if tid:
                    log_s = log_s + f" [{th.get_ident()}]"
                if fname:
                    log_s = log_s + f" func[{f.__name__}]"
                if len(top_word):
                    log_s = log_s + f" {top_word}"
                if inputval:
                    if inputval_func:
                        log_s = (
                            log_s
                            + f" args[{inputval_func(*args, **keywords)}]"
                        )
                    else:
                        log_s = log_s + f" args[{args}] keywords[{keywords}]"
                print(log_s)

            ret = f(*args, **keywords)

            if pos != LogPosition.HEAD:
                time_e = datetime.datetime.now()
                log_e = f"[{level.name}]"
                if timestamp:
                    log_e = log_e + f" {time_e}"
                if tid:
                    log_e = log_e + f" [{th.get_ident()}]"
                if fname:
                    log_e = log_e + f" func[{f.__name__}]"
                if len(bottom_word):
                    log_e = log_e + f" {bottom_word}"
                if elapsed_time:
                    log_e = log_e + f" elapsed time[{time_e - time_s}]"
                if retval:
                    if ret and retval_func:
                        v = retval_func(ret)
                        log_e = log_e + f" ret[{v}]"
                    else:
                        log_e = log_e + f" ret[{ret}]"
                print(log_e)

            return ret

        return _wrapper

    return _inner


def burger_log(
    level: LogLevel = LogLevel.INFO,
    timestamp: bool = True,
    elapsed_time: bool = False,
    fname: bool = False,
    tid: bool = False,
    inputval: bool = False,
    inputval_func: Optional[Callable] = None,
    retval: bool = False,
    retval_func: Optional[Callable] = None,
    top_word: str = "",
    bottom_word: str = "",
) -> Callable:
    return _log(
        level=level,
        pos=LogPosition.BURGER,
        timestamp=timestamp,
        elapsed_time=elapsed_time,
        fname=fname,
        tid=tid,
        inputval=inputval,
        inputval_func=inputval_func,
        retval=retval,
        retval_func=retval_func,
        top_word=top_word,
        bottom_word=bottom_word,
    )


def top_log(
    level: LogLevel = LogLevel.INFO,
    timestamp: bool = True,
    fname: bool = False,
    tid: bool = False,
    inputval: bool = False,
    inputval_func: Optional[Callable] = None,
    word: str = "",
) -> Callable:
    return _log(
        level=level,
        pos=LogPosition.HEAD,
        timestamp=timestamp,
        fname=fname,
        tid=tid,
        inputval=inputval,
        inputval_func=inputval_func,
        top_word=word,
    )


def bottom_log(
    level: LogLevel = LogLevel.INFO,
    timestamp: bool = True,
    elapsed_time: bool = False,
    fname: bool = False,
    tid: bool = False,
    retval: bool = False,
    retval_func: Optional[Callable] = None,
    word: str = "",
) -> Callable:
    return _log(
        level=level,
        pos=LogPosition.BOTTOM,
        timestamp=timestamp,
        elapsed_time=elapsed_time,
        fname=fname,
        tid=tid,
        retval=retval,
        retval_func=retval_func,
        bottom_word=word,
    )
