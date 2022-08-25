from test.support import captured_stdout

from function_burger import bottom_log, burger_log


def test_bottom_show_retval() -> None:
    @bottom_log(retval=True, timestamp=False, word="bottom")
    def func() -> str:
        return "ret_val"

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] bottom ret[ret_val]\n"


def test_bottom_hide_retval() -> None:
    @bottom_log(retval=False, timestamp=False, word="bottom")
    def func() -> str:
        return "ret_val"

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] bottom\n"


def test_burger_show_retval() -> None:
    @burger_log(
        retval=True, timestamp=False, top_word="top", bottom_word="bottom"
    )
    def func() -> str:
        return "ret_val"

    with captured_stdout() as stdout:
        func()

    output = "[INFO] top\n"
    output = output + "[INFO] bottom ret[ret_val]\n"
    assert stdout.getvalue() == output
