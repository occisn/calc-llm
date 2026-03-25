# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**calc-llm** teaches an LLM to solve math problems using GNU Emacs Calc through stack-based RPN keyboard macros. Algebraic expressions are avoided, even if equivalences may be proposed.

The project provides:
- A comprehensive Calc RPN command reference (`docs/calc-reference.md`)
- 8 worked examples with annotated and compact macros (`docs/examples.md`)
- An Elisp bridge to run macros via `emacs --batch`

Related projects:
- [calc-problem-solving](https://github.com/occisn/calc-problem-solving) — the original collection of solved Project Euler problems
- [cl-lisp2calc](https://github.com/occisn/cl-lisp2calc) — Common Lisp to Calc compiler

## Solving a Math Problem

When the user poses a math problem, **automatically read** `docs/calc-reference.md` and `docs/examples.md` before writing any macro. Do not wait for the user to mention these files — they are always the starting point.

Every solution must include:
1. **Annotated macro** — keystroke groups with `;; stack state` comments showing the stack after each step
2. **Compact macro** — single runnable line (strip comments, collapse whitespace)
3. **Result** — run the compact macro via `emacs --batch` and report the output

## Commands

**Test a macro:**
```
emacs --batch -l elisp/calc-runner.el -f calc-runner--main "2 RET 3 +"
```

## Project Structure

```
CLAUDE.md               — this file
docs/calc-reference.md  — Calc RPN command reference
docs/examples.md        — 8 worked examples
elisp/calc-runner.el    — Elisp bridge (emacs --batch)
```

## Conventions

- Follow workspace conventions from the parent CLAUDE.md
- Do not add Co-Authored-By lines to commit messages
- Always confirm the commit message with the user before committing
- **Knowledge accumulation:** whenever you discover something new about Calc (a command, idiom, pitfall, workaround, or trick), add it to `docs/calc-reference.md` so future queries benefit from it
