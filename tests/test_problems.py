"""Parametrized tests for all problem macros."""

import pytest
from src.runner import CalcRunner
from src.problems import PROBLEMS

runner = CalcRunner()


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p.id)
def test_problem(problem):
    """Run a problem's macro and verify result, status, and clean stack."""
    result = runner.run_macro(problem.macro)
    assert result.status == "ok", f"Macro failed: {result.error}"
    assert result.result == problem.expected, (
        f"Expected {problem.expected}, got {result.result}"
    )
    assert result.stack_depth == 1, (
        f"Stack not clean: {result.stack_depth} elements remaining"
    )
