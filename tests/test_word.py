# function-burger 🍔 by shinya_sun_sun, MIT license

from test.support import captured_stdout

from function_burger import bottom_log, burger_log, top_log


def test_top_show_top_word() -> None:
    @top_log(timestamp=False, word="top")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] top\n"


def test_top_hide_top_word() -> None:
    @top_log(timestamp=False, word="")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO]\n"


def test_top_def_top_word() -> None:
    @top_log(timestamp=False)
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO]\n"


def test_bottom_show_bottom_word() -> None:
    @bottom_log(timestamp=False, word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] bottom\n"


def test_bottom_hide_bottom_word() -> None:
    @bottom_log(timestamp=False, word="")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO]\n"


def test_bottom_def_bottom_word() -> None:
    @bottom_log(timestamp=False)
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO]\n"


def test_burger_top_bottom_word() -> None:
    @burger_log(timestamp=False, top_word="top", bottom_word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] top\n[INFO] bottom\n"
