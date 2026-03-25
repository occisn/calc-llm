"""Unit tests for the Calc macro runner."""

import pytest
from src.runner import CalcRunner

runner = CalcRunner()


def test_simple_addition():
    result = runner.run_macro("2 RET 3 +")
    assert result.status == "ok"
    assert result.result == "5"
    assert result.stack_depth == 1


def test_simple_multiplication():
    result = runner.run_macro("7 RET 6 *")
    assert result.status == "ok"
    assert result.result == "42"


def test_stack_depth():
    result = runner.run_macro("1 SPC 2 SPC 3")
    assert result.status == "ok"
    assert result.stack_depth == 3
    assert result.result == "3"  # top of stack


def test_large_number():
    result = runner.run_macro("2 SPC 1000 ^")
    assert result.status == "ok"
    assert result.result.startswith("107150860")
    assert result.stack_depth == 1


def test_vector_operations():
    result = runner.run_macro("v x 5 RET")
    assert result.status == "ok"
    assert result.result == "[1, 2, 3, 4, 5]"


def test_empty_macro():
    result = runner.run_macro("")
    assert result.status == "error"
    assert "empty" in result.error.lower() or "Stack" in result.error


def test_integer_division():
    result = runner.run_macro("17 RET 5 \\")
    assert result.status == "ok"
    assert result.result == "3"


def test_modulo():
    result = runner.run_macro("17 RET 5 %")
    assert result.status == "ok"
    assert result.result == "2"


def test_factorial():
    result = runner.run_macro("10 !")
    assert result.status == "ok"
    assert result.result == "3628800"
