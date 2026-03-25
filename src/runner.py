"""Python wrapper around emacs --batch for running Calc keyboard macros."""

import json
import os
import subprocess
from dataclasses import dataclass


@dataclass
class CalcResult:
    """Result of running a Calc keyboard macro."""
    status: str          # "ok" or "error"
    result: str | None
    stack_depth: int
    duration_ms: int
    error: str | None


# Path to calc-runner.el relative to this file
_ELISP_PATH = os.path.join(os.path.dirname(__file__), "..", "elisp", "calc-runner.el")


class CalcRunner:
    """Run Emacs Calc keyboard macros in batch mode."""

    def __init__(self, emacs_path: str = "emacs", timeout: int = 120):
        self.emacs_path = emacs_path
        self.timeout = timeout
        self.elisp_path = os.path.abspath(_ELISP_PATH)

    def run_macro(self, macro: str) -> CalcResult:
        """Run a Calc keyboard macro string and return the result.

        The macro uses edmacro format (e.g. "2 RET 3 +", "v x 20 RET v R k l").
        """
        cmd = [
            self.emacs_path, "--batch",
            "-l", self.elisp_path,
            "-f", "calc-runner--main",
            macro,
        ]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout + 10,  # extra margin beyond elisp timeout
            )
        except subprocess.TimeoutExpired:
            return CalcResult(
                status="error", result=None, stack_depth=0,
                duration_ms=0, error="Subprocess timeout",
            )

        stdout = proc.stdout.strip()
        if not stdout:
            stderr = proc.stderr.strip()
            return CalcResult(
                status="error", result=None, stack_depth=0,
                duration_ms=0, error=f"No output from emacs (exit {proc.returncode}): {stderr[:200]}",
            )

        try:
            data = json.loads(stdout)
        except json.JSONDecodeError as e:
            return CalcResult(
                status="error", result=None, stack_depth=0,
                duration_ms=0, error=f"JSON parse error: {e}. Output: {stdout[:200]}",
            )

        return CalcResult(
            status=data.get("status", "error"),
            result=data.get("result"),
            stack_depth=data.get("stack_depth", 0),
            duration_ms=data.get("duration_ms", 0),
            error=data.get("error"),
        )
