# function-burger 🍔 by shinya_sun_sun, MIT license

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
    TOP = auto()
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

            bk_e = None
            try:
                ret = f(*args, **keywords)
            except Exception as e:
                bk_e = e
                raise e
            finally:
                if pos != LogPosition.TOP:
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
                    if bk_e:
                        log_e = log_e + f" except[{bk_e}]"
                    elif retval:
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
    """Output logs before and after each function call.

    Args:
        level (LogLevel, optional): Specify the log level.
        timestamp (bool, optional): Specify timestamp output.
        elapsed_time (bool, optional): Specify elapsed time output.
        fname (bool, optional): Specifies the output of the function name.
        tid (bool, optional): Specifies the output of the thread ID.
        inputval (bool, optional): Specifies the output of the input value.
        inputval_func (Optional[Callable], optional):
            Specifies a function to edit the output format of input values.
        retval (bool, optional): Specifies the output of the return value.
        retval_func (Optional[Callable], optional):
            Specifies a function to edit the output format of the return value.
        word (str, optional): Specifies the string to be output to the log.
        top_word (str, optional):
            Specifies the string to be output to the log
            before the function call.
        bottom_word (str, optional):
            Specifies the string to be output to the log
            after a function call.

    Returns:
        Callable: log output function.
    """
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
    """Output log before function call.

    Args:
        level (LogLevel, optional): Specify the log level.
        timestamp (bool, optional): Specify timestamp output.
        fname (bool, optional): Specifies the output of the function name.
        tid (bool, optional): Specifies the output of the thread ID.
        inputval (bool, optional): Specifies the output of the input value.
        inputval_func (Optional[Callable], optional):
            Specifies a function to edit the output format of input values.
        word (str, optional): Specifies the string to be output to the log.

    Returns:
        Callable: log output function.
    """
    return _log(
        level=level,
        pos=LogPosition.TOP,
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
    """Output log after function call.

    Args:
        level (LogLevel, optional): Specify the log level.
        timestamp (bool, optional): Specify timestamp output.
        elapsed_time (bool, optional): Specify elapsed time output.
        fname (bool, optional): Specifies the output of the function name.
        tid (bool, optional): Specifies the output of the thread ID.
        retval (bool, optional): Specifies the return output.
        retval_func (Optional[Callable], optional):Specifies the function
            to edit the output value of the return value.
        word (str, optional): Specifies the string to be output to the log.

    Returns:
        Callable: log output function.
    """
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
