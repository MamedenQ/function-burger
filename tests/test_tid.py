# function-burger 🍔 by shinya_sun_sun, MIT license

import threading as th
from test.support import captured_stdout

from function_burger import bottom_log, burger_log, top_log


def test_top_show_tid() -> None:
    @top_log(tid=True, timestamp=False, word="top")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == f"[INFO] [{th.get_ident()}] top\n"


def test_top_show_tid_other_th() -> None:
    @top_log(tid=True, timestamp=False, word="top")
    def func() -> None:
        pass

    t = th.Thread(target=func)
    with captured_stdout() as stdout:
        t.start()
        t.join()

    assert stdout.getvalue() == f"[INFO] [{t.ident}] top\n"


def test_top_hide_tid() -> None:
    @top_log(tid=False, timestamp=False, word="top")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] top\n"


def test_bottom_show_tid() -> None:
    @bottom_log(tid=True, timestamp=False, word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == f"[INFO] [{th.get_ident()}] bottom\n"


def test_bottom_hide_tid() -> None:
    @bottom_log(tid=False, timestamp=False, word="bottom")
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    assert stdout.getvalue() == "[INFO] bottom\n"


def test_burger_show_tid() -> None:
    @burger_log(
        tid=True, timestamp=False, top_word="top", bottom_word="bottom"
    )
    def func() -> None:
        pass

    with captured_stdout() as stdout:
        func()

    output = f"[INFO] [{th.get_ident()}] top\n"
    output = output + f"[INFO] [{th.get_ident()}] bottom\n"

    assert stdout.getvalue() == output
