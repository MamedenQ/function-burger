# function-burger 🍔 by shinya_sun_sun, MIT license

from test.support import captured_stdout

import pytest
from function_burger import LogLevel, bottom_log, top_log


@pytest.mark.parametrize(
    "level, ans",
    [
        (LogLevel.INFO, "INFO"),
        (LogLevel.WARN, "WARN"),
        (LogLevel.ERROR, "ERROR"),
        (LogLevel.VERBOSE, "VERBOSE"),
    ],
)
def test_top_level(level: LogLevel, ans: str) -> None:
    @top_log(level=level, timestamp=False, word="top")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert (
        stdout.getvalue() == f"{level.value[0]}[{ans}]{level.value[1]} top\n"
    )


@pytest.mark.parametrize(
    "level, ans",
    [
        (LogLevel.INFO, "INFO"),
        (LogLevel.WARN, "WARN"),
        (LogLevel.ERROR, "ERROR"),
        (LogLevel.VERBOSE, "VERBOSE"),
    ],
)
def test_bottom_level(level: LogLevel, ans: str) -> None:
    @bottom_log(level=level, timestamp=False, word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert (
        stdout.getvalue()
        == f"{level.value[0]}[{ans}]{level.value[1]} bottom\n"
    )
