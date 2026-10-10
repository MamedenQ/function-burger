"""Regression tests for decorator transparency and best-effort logging."""

import inspect
import traceback
from unittest.mock import Mock

import pytest

from function_burger import bottom_log, burger_log, top_log


DECORATORS = (top_log, bottom_log, burger_log)
RETURN_DECORATORS = (bottom_log, burger_log)


@pytest.mark.parametrize("decorator", RETURN_DECORATORS)
@pytest.mark.parametrize("value", [0, False, "", [], None])
def test_retval_func_receives_falsy_values(decorator, value, capsys):
    formatter = Mock(return_value="formatted")

    @decorator(timestamp=False, retval=True, retval_func=formatter)
    def original():
        return value

    assert original() is value
    formatter.assert_called_once_with(value)
    expected = "[INFO] ret[formatted]\n"
    if decorator is burger_log:
        expected = "[INFO]\n" + expected
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize("decorator", RETURN_DECORATORS)
def test_retval_func_is_not_called_when_retval_disabled(decorator, capsys):
    formatter = Mock()
    result = object()

    @decorator(timestamp=False, retval=False, retval_func=formatter)
    def original():
        return result

    assert original() is result
    formatter.assert_not_called()


@pytest.mark.parametrize("decorator", RETURN_DECORATORS)
def test_retval_func_does_not_require_truthy_callable(decorator, capsys):
    class Formatter:
        def __bool__(self):
            return False

        def __call__(self, value):
            return "formatted"

    @decorator(timestamp=False, retval=True, retval_func=Formatter())
    def original():
        return 0

    assert original() == 0
    assert "ret[formatted]" in capsys.readouterr().out


@pytest.mark.parametrize("decorator", DECORATORS)
def test_decorator_preserves_function_metadata(decorator, capsys):
    def original(value: int, *, suffix: str = "!") -> str:
        """Format a value with a suffix."""
        return str(value) + suffix

    original.custom_attribute = "preserved"
    wrapped = decorator(timestamp=False)(original)

    assert wrapped.__name__ == original.__name__
    assert wrapped.__qualname__ == original.__qualname__
    assert wrapped.__module__ == original.__module__
    assert wrapped.__doc__ == original.__doc__
    assert wrapped.__annotations__ == original.__annotations__
    assert wrapped.custom_attribute == "preserved"
    assert inspect.signature(wrapped) == inspect.signature(original)
    assert wrapped.__wrapped__ is original
    assert inspect.unwrap(wrapped) is original
    assert wrapped(3, suffix="?") == "3?"


@pytest.mark.parametrize("decorator", DECORATORS)
def test_reraise_preserves_exception_and_traceback(decorator, capsys):
    error = ValueError("original error")

    @decorator(timestamp=False)
    def original():
        raise error

    with pytest.raises(ValueError) as caught:
        original()

    assert caught.value is error
    frames = traceback.extract_tb(caught.value.__traceback__)
    assert [frame.name for frame in frames] == [
        "test_reraise_preserves_exception_and_traceback",
        "_wrapper",
        "original",
    ]


@pytest.mark.parametrize(
    "decorator, fail_at",
    [(top_log, 1), (bottom_log, 1), (burger_log, 1), (burger_log, 2)],
)
@pytest.mark.parametrize("raises", [False, True])
def test_print_failure_preserves_function_outcome(
    decorator, fail_at, raises, monkeypatch
):
    error = ValueError("original error")
    result = object()
    calls = []

    def fail_print(*args, **kwargs):
        if printer.call_count == fail_at:
            raise OSError("log failed")

    printer = Mock(side_effect=fail_print)
    monkeypatch.setattr("builtins.print", printer)

    @decorator(timestamp=False)
    def original():
        calls.append("called")
        if raises:
            raise error
        return result

    if raises:
        with pytest.raises(ValueError) as caught:
            original()
        assert caught.value is error
    else:
        assert original() is result
    assert calls == ["called"]
    assert printer.call_count == (2 if decorator is burger_log else 1)


@pytest.mark.parametrize("decorator", (top_log, burger_log))
@pytest.mark.parametrize("raises", [False, True])
def test_input_formatter_failure_preserves_function_outcome(
    decorator, raises, capsys
):
    error = ValueError("original error")
    result = object()
    formatter = Mock(side_effect=RuntimeError("format failed"))

    @decorator(timestamp=False, inputval=True, inputval_func=formatter)
    def original(value):
        if raises:
            raise error
        return value

    if raises:
        with pytest.raises(ValueError) as caught:
            original(result)
        assert caught.value is error
    else:
        assert original(result) is result
    formatter.assert_called_once_with(result)


@pytest.mark.parametrize("decorator", RETURN_DECORATORS)
def test_return_formatter_failure_preserves_return_value(decorator, capsys):
    result = object()
    formatter = Mock(side_effect=RuntimeError("format failed"))

    @decorator(timestamp=False, retval=True, retval_func=formatter)
    def original():
        return result

    assert original() is result
    formatter.assert_called_once_with(result)


@pytest.mark.parametrize("decorator", RETURN_DECORATORS)
def test_return_string_failure_preserves_return_value(decorator, capsys):
    class Unprintable:
        def __str__(self):
            raise RuntimeError("format failed")

    result = Unprintable()

    @decorator(timestamp=False, retval=True)
    def original():
        return result

    assert original() is result


@pytest.mark.parametrize("decorator", RETURN_DECORATORS)
def test_exception_string_failure_preserves_exception(decorator, capsys):
    class UnprintableError(Exception):
        def __str__(self):
            raise RuntimeError("format failed")

    error = UnprintableError()

    @decorator(timestamp=False, retval=True)
    def original():
        raise error

    with pytest.raises(UnprintableError) as caught:
        original()
    assert caught.value is error


@pytest.mark.parametrize("decorator", RETURN_DECORATORS)
@pytest.mark.parametrize("error_type", [KeyboardInterrupt, SystemExit])
def test_base_exception_is_not_masked_by_return_logging(
    decorator, error_type, capsys
):
    error = error_type("original error")
    formatter = Mock()

    @decorator(timestamp=False, retval=True, retval_func=formatter)
    def original():
        raise error

    with pytest.raises(error_type) as caught:
        original()
    assert caught.value is error
    formatter.assert_not_called()
