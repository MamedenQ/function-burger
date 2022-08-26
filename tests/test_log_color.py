# function-burger 🍔 by shinya_sun_sun, MIT license

from test.support import captured_stdout

import pytest
from function_burger import LogColor, bottom_log, top_log


@pytest.mark.parametrize(
    "color",
    [
        (LogColor.VANILLA_SHAKE),
        (LogColor.MUSTARD),
        (LogColor.KETCHUP),
        (LogColor.MINT_CHOCOLATE),
        (LogColor.SODA),
        (LogColor.LETTUCE),
        (LogColor.GRAPE_JUICE),
        (LogColor.COLA),
    ],
)
def test_top_color(color: LogColor) -> None:
    @top_log(color=color, timestamp=False, word="top")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == f"[INFO]{color.value[0]} top{color.value[1]}\n"


@pytest.mark.parametrize(
    "color",
    [
        (LogColor.VANILLA_SHAKE),
        (LogColor.MUSTARD),
        (LogColor.KETCHUP),
        (LogColor.MINT_CHOCOLATE),
        (LogColor.SODA),
        (LogColor.LETTUCE),
        (LogColor.GRAPE_JUICE),
        (LogColor.COLA),
    ],
)
def test_bottom_color(color: LogColor) -> None:
    @bottom_log(color=color, timestamp=False, word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert (
        stdout.getvalue() == f"[INFO]{color.value[0]} bottom{color.value[1]}\n"
    )
