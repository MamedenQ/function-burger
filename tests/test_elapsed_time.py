# function-burger 🍔 by shinya_sun_sun, MIT license

import datetime
from test.support import captured_stdout
from typing import Any
from unittest.mock import patch

from function_burger import bottom_log, burger_log

dt_mock = datetime.datetime(2022, 8, 25, 14, 25, 30, 2002)
dt_mock_bottom = datetime.datetime(2022, 8, 25, 14, 25, 30, 2012)


@patch("datetime.datetime")
def test_bottom_show_elapsed_time(dt: Any) -> None:
    dt.now.side_effect = [dt_mock, dt_mock_bottom]

    @bottom_log(timestamp=False, elapsed_time=True, tid=False, word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] bottom elapsed time[0:00:00.000010]\n"


@patch("datetime.datetime")
def test_bottom_hide_elapsed_time(dt: Any) -> None:
    dt.now.side_effect = [dt_mock, dt_mock_bottom]

    @bottom_log(timestamp=False, elapsed_time=False, tid=False, word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] bottom\n"


@patch("datetime.datetime")
def test_burger_elapsed_time(dt: Any) -> None:
    dt.now.side_effect = [dt_mock, dt_mock_bottom]

    @burger_log(
        timestamp=False,
        elapsed_time=True,
        tid=False,
        top_word="top",
        bottom_word="bottom",
    )
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    output = "[INFO] top\n"
    output = output + "[INFO] bottom elapsed time[0:00:00.000010]\n"

    assert stdout.getvalue() == output
