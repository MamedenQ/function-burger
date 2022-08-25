# function-burger 🍔 by shinya_sun_sun, MIT license

from test.support import captured_stdout

from function_burger import bottom_log, burger_log, top_log


def test_top() -> None:
    @top_log(timestamp=False, word="top")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] top\n"


def test_bottom() -> None:
    @bottom_log(timestamp=False, word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] bottom\n"


def test_burger() -> None:
    @burger_log(timestamp=False, top_word="top", bottom_word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] top\n[INFO] bottom\n"
