# function-burger 🍔 by shinya_sun_sun, MIT license

import datetime
from test.support import captured_stdout
from typing import Any
from unittest.mock import patch

from function_burger import bottom_log, burger_log, top_log

dt_mock = datetime.datetime(2022, 8, 25, 14, 25, 30, 2002)
dt_mock_bottom = datetime.datetime(2023, 8, 25, 14, 25, 30, 2002)


@patch("datetime.datetime")
def test_top_def(dt: Any) -> None:
    dt.now.return_value = dt_mock

    @top_log()
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] 2022-08-25 14:25:30.002002\n"


@patch("datetime.datetime")
def test_bottom_def(dt: Any) -> None:
    dt.now.return_value = dt_mock_bottom

    @bottom_log()
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] 2023-08-25 14:25:30.002002\n"


@patch("datetime.datetime")
def test_burger_def(dt: Any) -> None:
    dt.now.side_effect = [dt_mock, dt_mock_bottom]

    @burger_log()
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    output = "[INFO] 2022-08-25 14:25:30.002002\n"
    output = output + "[INFO] 2023-08-25 14:25:30.002002\n"

    assert stdout.getvalue() == output
