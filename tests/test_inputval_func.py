from test.support import captured_stdout

from function_burger import burger_log, top_log


def test_top_lambda_inputval_func() -> None:
    @top_log(
        inputval=True,
        inputval_func=lambda *a, **k: f"--{a[0]}--{k['c']}--",
        timestamp=False,
        word="top",
    )
    def func(a: int, b: int, *, c: int, d: int) -> None:
        pass

    with captured_stdout() as stdout:
        func(1, 2, c=3, d=4)

    assert stdout.getvalue() == "[INFO] top args[--1--3--]\n"


def test_top_none_inputval_func() -> None:
    @top_log(
        inputval=True,
        inputval_func=None,
        timestamp=False,
        word="top",
    )
    def func(a: int, b: int, *, c: int, d: int) -> None:
        pass

    with captured_stdout() as stdout:
        func(1, 2, c=3, d=4)

    assert (
        stdout.getvalue()
        == "[INFO] top args[(1, 2)] keywords[{'c': 3, 'd': 4}]\n"
    )


def test_burger_lambda_inputval_func() -> None:
    @burger_log(
        inputval=True,
        inputval_func=lambda *a, **k: f"--{a[0]}--{k['c']}--",
        timestamp=False,
        top_word="top",
        bottom_word="bottom",
    )
    def func(a: int, b: int, *, c: int, d: int) -> None:
        pass

    with captured_stdout() as stdout:
        func(1, 2, c=3, d=4)

    output = "[INFO] top args[--1--3--]\n"
    output = output + "[INFO] bottom\n"

    assert stdout.getvalue() == output
