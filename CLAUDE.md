# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**calc-llm** teaches an LLM to solve math problems using GNU Emacs Calc through stack-based RPN keyboard macros. Algebraic expressions are avoided, even if equivalences may be proposed.

The project provides:
- A comprehensive Calc RPN command reference (`docs/calc-reference.md`)
- 8 worked examples with annotated and compact macros (`docs/examples.md`)
- A Python testing harness that validates macros via `emacs --batch`

Related projects:
- [calc-problem-solving](https://github.com/occisn/calc-problem-solving) — the original collection of solved Project Euler problems
- [cl-lisp2calc](https://github.com/occisn/cl-lisp2calc) — Common Lisp to Calc compiler

## Solving a Math Problem

See `docs/calc-reference.md` for the full methodology, rules, and command reference.
See `docs/examples.md` for 8 worked Project Euler solutions.

## Commands

**Run all tests:**
```
python3 -m pytest tests/ -v
```

**Run only runner tests:**
```
python3 -m pytest tests/test_runner.py -v
```

**Run only problem tests:**
```
python3 -m pytest tests/test_problems.py -v
```

**Test a single problem:**
```
python3 -m pytest tests/test_problems.py -v -k euler_003
```

**Quick one-off macro test:**
```
python3 -c "from src.runner import CalcRunner; r = CalcRunner(); print(r.run_macro('2 RET 3 +'))"
```

**Direct emacs test:**
```
emacs --batch -l elisp/calc-runner.el -f calc-runner--main "2 RET 3 +"
```

## Adding a New Problem

1. Add a `Problem(...)` entry to `src/problems.py` with the compact macro and expected answer
2. Run `python3 -m pytest tests/test_problems.py -v -k new_problem_id`
3. Verify: status is "ok", result matches, stack_depth is 1

## Project Structure

```
CLAUDE.md               — this file
docs/calc-reference.md  — Calc RPN command reference
docs/examples.md        — 8 worked examples
elisp/calc-runner.el    — Elisp bridge (emacs --batch)
src/runner.py           — Python CalcRunner class
src/problems.py         — Problem definitions
tests/test_runner.py    — Runner unit tests
tests/test_problems.py  — Parametrized problem tests
```

## Conventions

- Follow workspace conventions from the parent CLAUDE.md
- Do not add Co-Authored-By lines to commit messages
- Always confirm the commit message with the user before committing
- **Knowledge accumulation:** whenever you discover something new about Calc (a command, idiom, pitfall, workaround, or trick), add it to `docs/calc-reference.md` so future queries benefit from it
