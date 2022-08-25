from test.support import captured_stdout

from function_burger import bottom_log, top_log


def test_top_show_fname() -> None:
    @top_log(fname=True, timestamp=False, word="top")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] func[func] top\n"


def test_top_hide_fname() -> None:
    @top_log(fname=False, timestamp=False, word="top")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] top\n"


def test_bottom_show_fname() -> None:
    @bottom_log(fname=True, timestamp=False, word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] func[func] bottom\n"


def test_bottom_hide_fname() -> None:
    @bottom_log(fname=False, timestamp=False, word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] bottom\n"
