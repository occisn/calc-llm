# calc-llm

Teaching an LLM to solve math problems using [GNU Emacs Calc](https://www.gnu.org/software/emacs/manual/html_mono/calc.html) through stack-based RPN keyboard macros. Algebraic expressions are avoided, even if equivalences may be proposed.

In the spirit of [calc-problem-solving](https://github.com/occisn/calc-problem-solving), which solves Project Euler puzzles with Calc keyboard macros. See also [cl-lisp2calc](https://github.com/occisn/cl-lisp2calc), a Common Lisp to Calc compiler.

## What's inside

- **[Calc RPN command reference](docs/calc-reference.md)** -- methodology, rules, and comprehensive command cheat sheet with reusable idioms
- **[8 worked examples](docs/examples.md)** -- Project Euler solutions with annotated and compact macros
- **Testing harness** -- Python + Elisp bridge that runs Calc macros via `emacs --batch` and verifies results automatically
- **Problem collection** -- 10 Project Euler solutions as testable problem definitions

## Requirements

- GNU Emacs 30+ (for `json-encode`)
- Python 3.10+
- pytest (`pip install -r requirements.txt`)

## Quick start

```bash
pip install -r requirements.txt
python3 -m pytest tests/ -v
```

One-off macro test:

```bash
python3 -c "from src.runner import CalcRunner; r = CalcRunner(); print(r.run_macro('v x 20 RET v R k l'))"
```

## How it works

1. `elisp/calc-runner.el` -- loads Calc in batch mode, parses a macro string with `edmacro-parse-keys`, executes it with `execute-kbd-macro`, outputs JSON with the result and stack state
2. `src/runner.py` -- Python wrapper that calls `emacs --batch`, parses the JSON output
3. `tests/test_problems.py` -- parametrized pytest suite that verifies each problem macro produces the correct answer with a clean stack

## Project structure

```
docs/calc-reference.md  -- Calc RPN command reference
docs/examples.md        -- 8 worked examples
elisp/calc-runner.el    -- Elisp bridge (emacs --batch)
src/runner.py           -- Python CalcRunner class
src/problems.py         -- Problem definitions
tests/test_runner.py    -- Runner unit tests
tests/test_problems.py  -- Parametrized problem tests
```

## Contributing

Open an [issue](https://github.com/occisn/calc-llm/issues) or start a [discussion](https://github.com/occisn/calc-llm/discussions).
