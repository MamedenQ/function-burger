from test.support import captured_stdout

from function_burger import burger_log, top_log


def test_top_show_inputval() -> None:
    @top_log(inputval=True, timestamp=False, word="top")
    def func(a: int, b: int, *, c: int, d: int) -> None:
        pass

    with captured_stdout() as stdout:
        func(1, 2, c=3, d=4)

    assert (
        stdout.getvalue()
        == "[INFO] top args[(1, 2)] keywords[{'c': 3, 'd': 4}]\n"
    )


def test_top_hide_inputval() -> None:
    @top_log(inputval=False, timestamp=False, word="top")
    def func(a: int, b: int, *, c: int, d: int) -> None:
        pass

    with captured_stdout() as stdout:
        func(1, 2, c=3, d=4)

    assert stdout.getvalue() == "[INFO] top\n"


def test_burger_show_inputval() -> None:
    @burger_log(
        inputval=True, timestamp=False, top_word="top", bottom_word="bottom"
    )
    def func(a: int, b: int, *, c: int, d: int) -> None:
        pass

    with captured_stdout() as stdout:
        func(1, 2, c=3, d=4)

    output = "[INFO] top args[(1, 2)] keywords[{'c': 3, 'd': 4}]\n"
    output = output + "[INFO] bottom\n"

    assert stdout.getvalue() == output
