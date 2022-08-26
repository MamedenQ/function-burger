# function-burger 🍔 by shinya_sun_sun, MIT license

from test.support import captured_stdout

from function_burger import bottom_log


def test_top_except() -> None:
    @bottom_log(timestamp=False)
    def func() -> None:
        e = Exception("except!!!")
        raise e

    with captured_stdout() as stdout:
        try:
            func()
        except Exception:
            pass

    assert (
        stdout.getvalue() == "[INFO] \033[7m\033[31mexcept[except!!!]\033[0m\n"
    )
