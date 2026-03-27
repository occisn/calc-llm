# calc-llm

Solve math problems with [GNU Emacs Calc](https://www.gnu.org/software/emacs/manual/html_mono/calc.html) RPN keyboard macros, powered by an LLM.

## Usage

Give a math problem to an LLM (e.g. Claude). The LLM uses the reference docs and examples as context to produce a Calc RPN macro that solves it. The macro is injected into Emacs in order to get the result.

For instance, "10,001st prime number" returns ~2 SPC 10001 SPC 1 - Z< k n Z>~ and 104743.

## Reference for LLM

The LLM uses:
- **[Calc RPN command reference](docs/calc-reference.md)** -- methodology, rules, and comprehensive command cheat sheet with reusable idioms
- **[8 examples of annotated and compact macros](docs/examples-of-annotated-and-compact-macros.md)**

## Running a macro

Paste a macro into Emacs, select it, run `M-x read-kbd-macro`, switch to Calc and press `X`.

Or test from the command line:

```bash
emacs --batch -l elisp/calc-runner.el -f calc-runner--main "2 RET 3 +"
```

## Project structure

```
docs/calc-reference.md  -- Calc RPN command reference
docs/examples-of-annotated-and-compact-macros.md -- 8 examples
elisp/calc-runner.el    -- Elisp bridge (emacs --batch)
```

## Related projects

- [calc-problem-solving](https://github.com/occisn/calc-problem-solving) -- the original collection of solved Project Euler problems with Calc
- [cl-lisp2calc](https://github.com/occisn/cl-lisp2calc) -- Common Lisp to Calc compiler

## Contributing

Open an [issue](https://github.com/occisn/calc-llm/issues) or start a [discussion](https://github.com/occisn/calc-llm/discussions).
