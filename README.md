# calc-llm

Solve math problems with [GNU Emacs Calc](https://www.gnu.org/software/emacs/manual/html_mono/calc.html) RPN keyboard macros, powered by an LLM.

## Usage

Give a math problem to an LLM (e.g. Claude). The LLM uses the reference docs and examples as context to produce a Calc RPN macro that solves it. The macro can then be tested within Emacs, either interactively or via the included batch harness.

For best results, point the LLM at:
- **[Calc RPN command reference](docs/calc-reference.md)** -- methodology, rules, and comprehensive command cheat sheet with reusable idioms
- **[8 worked examples](docs/examples.md)** -- Project Euler solutions with annotated and compact macros

## Running a macro

Paste a macro into Emacs, select it, run `M-x read-kbd-macro`, switch to Calc and press `X`.

Or test from the command line:

```bash
emacs --batch -l elisp/calc-runner.el -f calc-runner--main "2 RET 3 +"
```

## Testing harness

A Python + Elisp bridge runs Calc macros via `emacs --batch` and verifies results automatically. This is a development tool, not the main purpose of the project.

**Requirements:** GNU Emacs 30+, Python 3.10+

```bash
pip install -r requirements.txt
python3 -m pytest tests/ -v
```

## Project structure

```
docs/calc-reference.md  -- Calc RPN command reference
docs/examples.md        -- 8 worked examples
elisp/calc-runner.el    -- Elisp bridge (emacs --batch)
src/runner.py           -- Python CalcRunner class
src/problems.py         -- Problem definitions (10 Project Euler solutions)
tests/test_runner.py    -- Runner unit tests
tests/test_problems.py  -- Parametrized problem tests
```

## Related projects

- [calc-problem-solving](https://github.com/occisn/calc-problem-solving) -- the original collection of solved Project Euler problems with Calc
- [cl-lisp2calc](https://github.com/occisn/cl-lisp2calc) -- Common Lisp to Calc compiler

## Contributing

Open an [issue](https://github.com/occisn/calc-llm/issues) or start a [discussion](https://github.com/occisn/calc-llm/discussions).
