# function-burger 🍔 by shinya_sun_sun, MIT license

from test.support import captured_stdout

from function_burger import bottom_log, burger_log


def test_bottom_lambda_retval_func() -> None:
    @bottom_log(
        retval=True,
        retval_func=lambda a: f"--{a}--",
        timestamp=False,
        word="bottom",
    )
    def func() -> str:
        return "ret_val"

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] bottom ret[--ret_val--]\n"


def test_bottom_none_retval_func() -> None:
    @bottom_log(
        retval=True,
        retval_func=None,
        timestamp=False,
        word="bottom",
    )
    def func() -> str:
        return "ret_val"

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] bottom ret[ret_val]\n"


def test_burger_lambda_retval() -> None:
    @burger_log(
        retval=True,
        retval_func=lambda a: f"--{a}--",
        timestamp=False,
        top_word="top",
        bottom_word="bottom",
    )
    def func() -> str:
        return "ret_val"

    with captured_stdout() as stdout:
        func()

    output = "[INFO] top\n"
    output = output + "[INFO] bottom ret[--ret_val--]\n"
    assert stdout.getvalue() == output
