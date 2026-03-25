# GNU Emacs Calc RPN Command Reference

Comprehensive cheat sheet for writing Calc keyboard macros in RPN style. All commands use the stack-based (RPN) approach; algebraic entry (`'...`) is avoided.

Manual: https://www.gnu.org/software/emacs/manual/html_mono/calc.html

## Solving a Math Problem

### Methodology

1. **Analyze the problem** — identify the mathematical formula or algorithm
2. **Plan the stack layout** — decide which values go on the stack and in what order; draw the initial stack state
3. **Choose control flow** — select the appropriate loop type (`Z<Z>` for repeat-N, `Z(Z)` for counted for-loop, `Z{Z/Z}` for repeat-until) and conditionals (`Z[Z]` or `Z[Z:Z]`)
4. **Write the annotated macro** — keystroke groups with `;;` comments showing the stack state after each step
5. **Derive the compact macro** — strip comments and collapse into a single runnable line
6. **Verify** — mentally trace through the stack, or run via the test harness

### Output Format

Every solution must include:
- **Problem statement** (one-line summary)
- **Approach** (brief mathematical strategy)
- **Annotated macro** (with `;; stack state` comments)
- **Compact macro** (single runnable line)
- **Expected result**

### Key Rules

- **RPN only** — never use algebraic entry (`'...`). All arithmetic is stack-based: push operands first, then apply the operator.
- **`SPC` separates consecutive numbers** — e.g. `3 SPC 4` pushes 3 then 4. Not needed between a number and an operator (`3 RET 4 +` works because `+` auto-finalizes the `4`).
- **`RET` duplicates** — it does NOT mean "enter". Numbers are auto-pushed when the next command runs. `RET` copies the top element.
- **Clean stack** — the macro should leave exactly 1 element on the stack (the answer). Delete temporary values with `DEL`, `M-DEL`, etc.
- **Modulo forms** — when using `S-M` for modular arithmetic, unpack at the end with `v u DEL` to leave a plain integer.

---

## 1. Number Entry

```
123        type digits to enter a number (auto-pushed when next command runs)
SPC        separator between two consecutive numbers (e.g. "3 SPC 4")
_          negative sign prefix (e.g. "_5" enters -5)
.          decimal point (e.g. "3.14")
e          scientific notation (e.g. "6.02e23")
#          radix prefix (e.g. "16#FF" enters 255, "2#1010" enters 10)
:          fraction separator (e.g. "3:4" enters 3/4)
@          HMS form entry (e.g. "2@ 30' 15\"" enters 2 deg 30 min 15 sec)
..         interval separator (e.g. "[1 .. 10]")
p          error form separator (e.g. "100 p 0.5" enters 100 +/- 0.5)
M          modulo form (e.g. "6 M 24" enters 6 mod 24)
```

**Date forms:** Enter dates as `<Jul 4, 1992>`. Special values: `inf` (infinity), `nan` (indeterminate).

**Important:** `SPC` is needed only between two consecutive number entries. When a number is followed by an operator, the number is auto-finalized.

## 2. Stack Manipulation

```
RET          duplicate top element (copy #1)
C-u 2 RET   duplicate top 2 elements
C-u N RET   duplicate top N elements
C-j          copy element #2 to top (synonym: LFD)
C-u N C-j    copy element #N to top
TAB          swap elements #1 and #2
C-u N TAB    rotate down: #1 moves to position #N, elements #2..#N move up
M-TAB        rotate up: element #3 moves to #1 (synonym: C-M-i)
C-u N C-M-i  rotate up: element #N moves to #1, elements #1..#(N-1) move down
DEL          delete top element
C-d          synonym for DEL
M-DEL        delete element #2
C-u N M-DEL  delete element #N
C-u 0 DEL   clear entire stack
C-u 0 TAB   reverse entire stack
M-RET        push last arguments (the args consumed by the previous command)
K            keep-arguments prefix: next command does not consume its stack args
U            undo last operation
D            redo last operation
w            display recent error messages
```

**Prefix argument `~`:** uses top-of-stack as the numeric prefix (consuming it). E.g. `~ C-j` copies the element at position given by the (consumed) top value.

**Derived idioms:**
```
C-u 3 C-M-i C-u 4 TAB                              swap elements #3 and #4
C-u 4 C-M-i 1 + C-u 4 TAB                          add 1 to element #4
C-u 4 C-M-i + C-u 3 TAB                             pop top and add it to (original) element #4
C-u 4 C-M-i C-u 2 RET a> Z[ DEL RET Z] C-u 4 TAB   replace element #4 with #1 if #1 > #4
```

**Caution:** `~ C-j` copies the N-th element *after* the top has been consumed, so the numbering shifts by one.

## 3. Arithmetic

```
+      add
-      subtract
*      multiply
/      divide
\      integer division
%      modulo
:      fractional divide (integer division yielding exact fraction)
^      power
I^     n-th root
I Q    square (x^2)
n      negate (-x)
A      absolute value
&      reciprocal (1/x)
Q      square root
f Q    integer square root
F      floor
I F    ceiling (round toward +inf)
R      round to nearest integer
I R    truncate toward zero
H F    floor as float
H I F  ceiling as float
H R    round as float
H I R  truncate as float
!      factorial
f S    scale by power of 10 (x * 10^y)
f n    min(#2, #1)
f x    max(#2, #1)
f s    sign: returns -1, 0, or 1
f h    hypotenuse: sqrt(a^2 + b^2)
f [    decrement by 1 (or by prefix arg)
f ]    increment by 1 (or by prefix arg)
f M    extract mantissa of float
f X    extract exponent of float
c 2    round off last two digits
c F    convert to fraction
c f    convert to float
c %    convert to percentage
```

## 4. Logarithms and Exponentials

```
L      ln (natural log)
H L    log10
E      exp (e^x)
H E    exp10 (10^x)
B      log to arbitrary base: log_b(a) — consumes 2 (a, b)
I B    anti-log: b^a — consumes 2
f I    integer log to arbitrary base — consumes 2
f E    expm1: exp(x)-1, accurate near zero
f L    lnp1: ln(x+1), accurate near zero
```

## 5. Number Theory

```
k f             prime factorization → vector (e.g. 12 → [2, 2, 3])
k n             next prime after top element
I k n           previous prime before top element
k p             primality test (prints result in echo area, does not consume)
'prime($1) RET  primality test → 0/1 on stack (consumes)
k g             GCD of top two elements
k l             LCM of top two elements
k E             extended GCD → [gcd, a, b] where gcd = a*x + b*y
k c             combinations C(n,r)
H k c           permutations P(n,r)
k t             Euler totient function φ(n)
k m             Möbius mu function μ(n)
k d             double factorial N!!
k b             Bernoulli number B_n
H k b           Bernoulli polynomial B_n(x)
k e             Euler number E_n
H k e           Euler polynomial E_n(x)
k s             Stirling number of the first kind
H k s           Stirling number of the second kind
k r             random number (range M from stack)
k h             shuffle (random permutation of vector)
k a             random-again: repeat last random with same params
```

**Largest prime factor:** `k f v v v r 1 RET`
**N-th prime:** `1 - 2 TAB Z< k n Z>`

## 6. Comparison and Logic

```
a =     1 if #2 = #1, else 0 (consumes both)
a #     1 if #2 ≠ #1, else 0 (consumes both)
a <     1 if #2 < #1, else 0 (consumes both)
a >     1 if #2 > #1, else 0 (consumes both)
a [     1 if #2 ≤ #1, else 0 (consumes both)
a ]     1 if #2 ≥ #1, else 0 (consumes both)
a &     logical AND (nonzero if both nonzero)
a |     logical OR (nonzero if either nonzero)
a !     logical NOT (1 if arg is 0, else 0)
a :     conditional if(a,b,c): if a≠0 then b, else c — consumes 3
a {     membership test: 1 if a is in set b
```

## 7. Vectors

### Creation and Access

```
v x N RET   iota: create vector [1, 2, ..., N]
C-u v x     counted vector: n values from a with step b — consumes 3 (n, a, b)
N v p       pack top N elements into a vector
v r N RET   extract element N from vector (1-indexed)
v l         length of vector
v v         reverse vector
v k         cons: prepend element to vector
H v k       rcons: append element to end of vector
|           concatenate two vectors (or append element)
v u         unpack (e.g. unpack modulo form, complex, or vector)
v h         head: first element of vector
I v h       tail: all but first element of vector
H v h       rhead: all but last element of vector
H I v h     rtail: last element of vector
v s         subvector: extract sub-range — consumes 3 (vec, start, end)
I v s       rsubvec: remove sub-range — consumes 3
v f         find element in vector → index or 0 — consumes 2
v b         build vector of N copies of value (N from prefix arg)
v c         extract matrix column
```

**Note:** In macros, `v r` prompts for an index; use `~ v r` to take the index from the stack (via `~` prefix).

### Reduce, Map, and Apply

```
v R op      reduce vector with binary op (e.g. v R + for sum, v R k l for LCM)
I v R op    right-reduce (fold from right)
V U op      accumulate (running reduce → vector of partial results)
I V U op    right-accumulate
V M op      map unary operator over vector
V M _ op    map by rows (row-wise)
V M : op    map by columns (column-wise)
V R _ op    reduce across rows
V R : op    reduce down columns
V A op      apply: use vector elements as function arguments
V O op      outer product of two vectors → matrix
V I op1 op2 inner (generalized) product of two vectors
H V R op    nest: apply function N times — consumes 2 (value, count)
H V U op    accumulating nest → vector of intermediate results
H I V R op  iterate to fixed point
H I V U op  accumulating fixed point → vector
```

### Sorting and Ordering

```
V S         sort vector ascending
I V S       sort vector descending
V G         grade: index permutation that would sort ascending
I V G       grade descending
V H         histogram (prefix arg = number of bins)
```

### Matrix Operations

```
v d         build diagonal matrix from vector (prefix arg = size)
v i         build identity matrix (prefix arg = size)
v a         arrange vector into matrix with N columns (prefix arg = N)
v t         transpose matrix
V J         conjugate transpose
V D         determinant of square matrix
&           matrix inverse (same key as reciprocal)
V T         trace of square matrix
V L         LU decomposition → vector of 3 matrices
V C         cross product of two 3-element vectors
V K         Kronecker product of two matrices
v n         infinity-norm / row-norm
V N         one-norm / column-norm
v m         mask vector: select elements where mask is nonzero
v e         expand vector using mask
```

### Set Operations (vectors as sets)

```
V +         remove duplicates (convert to set)
V V         set union
V ^         set intersection
V -         set difference
V X         set symmetric difference (XOR)
V ~         set complement w.r.t. reals
V #         set cardinality (count of integers in set)
V :         set span (interval from min to max)
```

## 8. Modulo Forms

```
2 S-M 25 SPC    enter 2 mod 25 (interactive: type 2M25)
C-u -5 v p      pack top two stack elements into modulo form
v u              unpack modulo form back to two elements
```

**Modular exponentiation:** Enter the base as a modulo form, then exponentiate.
```
2 S-M 10000000000 SPC 7830457 ^    → 2^7830457 mod 10000000000
```

## 9. Control Flow

### Conditional

```
Z[ body Z]          if top ≠ 0, execute body (top is consumed)
Z[ then Z: else Z]  if top ≠ 0, execute then; else execute else (top is consumed)
```

### Repeat N times

```
N Z< body Z>        execute body N times (N is consumed)
```

### For loop

```
lo hi Z( body step Z)   for i from lo to hi: push i, execute body, pop step
```

The loop counter is pushed at the start of each iteration. The body must leave one value on top which is consumed as the step (increment). Use `1 Z)` for step=1, `1 n Z)` for step=-1 (downward loop).

**Caveat:** The loop body must not be empty. A loop from 1 to 1 does not seem to work.

### Repeat-until

```
Z{ body Z/ rest Z}   execute body; if top ≠ 0 after Z/, break; else continue with rest
```

`Z/` tests the top element: if non-zero, exits the loop. The test value is consumed.

### Macro Environment

```
Z `     save mode settings and quick variables (begin local block)
Z '     restore mode settings and quick variables (end local block)
Z #     query user for input during macro (pushes result to stack)
Z C-g   break out of a loop or conditional immediately
```

### Programming

```
C-x (   begin recording a keyboard macro
C-x )   end recording a keyboard macro
X       replay keyboard macro
C-x * m read region as written-out macro
Z K     put finished macro on a key
Z F     define function with formula
Z E     edit definition
Z P     record user-defined command permanently
```

## 10. Store and Recall

```
s s            store top of stack into variable (prompts for name), does not pop
s t            store into variable and pop from stack
s 0-9          quick store into q0–q9 (same as s t 0-9), pops
s r            recall variable to stack (prompts for name)
r 0-9          quick recall from q0–q9
s +            add top-of-stack to variable (pops)
s -            subtract from variable (pops)
s *            multiply variable (pops)
s /            divide variable (pops)
s ^            exponentiate variable (pops)
s |            concatenate to variable (pops)
s n            negate variable (no stack arg)
s &            invert variable (no stack arg)
s [            decrement variable by 1
s ]            increment variable by 1
s x            exchange variable value with top of stack
s u            unstore (clear) a variable
s e            edit a variable
s l            let variable equal a value in formula (s l x=val)
s d            declare properties of variable (pos, int, real, scalar, [a..b])
s p            record variable value permanently
```

## 11. Constants

```
P              push π (3.14159...)
H P            push e (2.71828...)
I P            push Euler's gamma constant γ (0.5772...)
H I P          push golden ratio φ (1.6180...)
```

## 12. Trigonometry

```
S              sin
I S            arcsin
H S            sinh
H I S          arcsinh
C              cos
I C            arccos
H C            cosh
H I C          arccosh
T              tan
I T            arctan
H T            tanh
H I T          arctanh
f T            arctan2(y, x): full-range arctangent — consumes 2
```

All trig functions consume 1 and push 1 (except `f T` which consumes 2).

**Angular mode:**
```
m r            set Radians mode
m d            set Degrees mode
m h            set HMS mode
```

## 13. Complex Numbers

```
(a, b)          rectangular entry (e.g. "(3, 4)")
(r; θ)          polar entry (e.g. "(5; 30)")
C-u -1 v p      pack top 2 reals into rectangular complex
C-u -2 v p      pack top 2 into polar complex
v u              unpack complex into two reals
J                complex conjugate
G                argument (polar angle) of complex number
f r              real part
f i              imaginary part
c p              toggle rectangular/polar form
```

## 14. Binary and Bitwise Operations

```
b a            bitwise AND
b o            bitwise OR
b x            bitwise XOR
b n            bitwise NOT
b d            bitwise difference: and(a, not(b))
b c            clip to word size (reduce modulo 2^w)
b l            left shift by 1 bit (or prefix N bits)
b r            right shift by 1 bit (or prefix N bits)
b L            arithmetic left shift
b R            arithmetic right shift (sign-extending)
b t            rotate bits left by 1 (or prefix N)
H b l          left shift, shift count from stack — consumes 2
H b r          right shift, shift count from stack — consumes 2
H b L          arithmetic left shift, count from stack — consumes 2
H b R          arithmetic right shift, count from stack — consumes 2
H b t          rotate, count from stack — consumes 2
b w            set word size (prompts for value)
b p            pack set (vector) into binary integer
b u            unpack binary integer into set (vector)
```

**Display modes:**
```
d 2            display in binary
d 8            display in octal
d 6            display in hexadecimal
d 0            display in decimal (default)
```

## 15. Statistics

```
u #            count of data values
u +            sum of data values
u *            product of data values
u X            maximum
u N            minimum
u M            arithmetic mean
I u M          mean with estimated error (as error form)
H u M          median
H I u M        harmonic mean
u G            geometric mean
H u G          arithmetic-geometric mean of two numbers
u R            root-mean-square
u S            sample standard deviation
I u S          population standard deviation
H u S          sample variance
H I u S        population variance
u C            sample covariance of two vectors
I u C          population covariance
H u C          linear correlation coefficient
```

## 16. Financial Functions

```
M-%            enter percentage
c %            convert to percentage
b %            percentage change
b P            present value
b F            future value
b T            rate of return
b #            number of payments
b M            size of payments
b N            net present value
b I            internal rate of return
b S            straight-line depreciation
b Y            sum-of-years'-digits depreciation
b D            double declining balance depreciation
```

Above computations assume payments at end of period. Use `I` prefix for beginning of period, or `H` for a lump sum investment.

## 17. Probability Distributions

```
k B            upper-tail binomial — consumes 3 (n, p, x)
I k B          lower-tail binomial
k C            upper-tail chi-square — consumes 2 (v, x)
I k C          lower-tail chi-square
k F            upper-tail F-distribution — consumes 3 (v1, v2, x)
I k F          lower-tail F
k N            upper-tail normal (Gaussian) — consumes 3 (μ, σ, x)
I k N          lower-tail normal
k P            upper-tail Poisson — consumes 2 (λ, x)
I k P          lower-tail Poisson
k T            upper-tail Student's t — consumes 2 (v, x)
I k T          lower-tail Student's t
```

## 18. Advanced Math Functions

```
f g            gamma function Γ(x)
f G            incomplete gamma P(a,x) — consumes 2
I f G          complementary incomplete gamma Q(a,x)
H f G          lower incomplete gamma γ(a,x) (unnormalized)
H I f G        upper incomplete gamma Γ(a,x) (unnormalized)
f b            beta function B(a,b) — consumes 2
f B            incomplete beta I(x,a,b) — consumes 3
H f B          incomplete beta B(x,a,b) (unnormalized)
f e            error function erf(x)
I f e          complementary error function erfc(x)
f j            Bessel J function J_n(x) — consumes 2
f y            Bessel Y function Y_n(x) — consumes 2
```

## 19. Date and Time

```
t N            push current date/time
t D            convert number to date form, or date to number
t J            convert date to/from Julian day count
t U            convert date to/from Unix timestamp
t P            extract date part (prefix 1–9: year/month/day/hour/minute/second/weekday/yearday/time)
t M            first day of month (or Nth day with prefix)
t Y            first day of year (or Nth day with prefix)
t W            start of week (Sunday, or day given by prefix)
t I            increment month (prefix for step count)
t +            add business days — consumes 2
t -            subtract business days — consumes 2
```

## 20. Units and Conversions

```
u s            simplify units expression
u c            convert units (prompts for target units)
u n            convert units, requiring exact dimensional match
u b            convert to base (SI) units
u t            convert temperature (absolute)
u r            remove units from expression
u x            extract units only from expression
u v            view units table
```

**Common units:**
```
distance:    m, cm, mm, km; in, ft, mi, mfi; point, lyr
volume:      l or L, ml; gal, qt, pt, cup, floz, tbsp, tsp
mass:        g, mg, kg, t; lb, oz, ton
time:        s or sec, ms, us, ns, min, hr, day, wk
temperature: degC, degF, K
```

## 21. Algebraic Manipulation (RPN-usable)

```
a v            evaluate/simplify with default rules
=              evaluate, substituting stored variable values
N              evaluate numerically (disable Symbolic mode temporarily)
a s            simplify formula
a n            put formula into rational form
a e            extended (aggressive) simplification
a x            expand terms
a c            collect terms
a f            factor expression
a a            partial fractions
a \            polynomial quotient — consumes 2
a %            polynomial remainder — consumes 2
a g            polynomial GCD — consumes 2
a d            derivative w.r.t. prompted variable
a i            indefinite integral w.r.t. prompted variable
a I            numerical integration over a range
a t            Taylor series expansion
a S            solve equation for prompted variable (principal solution)
a P            list of solutions
H a S          generic solution
a M            apply function to both sides of equation
a R            numerical root-finding — consumes 2 (guess, expr)
a N            numerical minimization — consumes 2
a X            numerical maximization — consumes 2
a F            curve fit (linear regression etc.) — consumes 2 (x-data, y-data)
a +            summation over variable (prompts for var and limits)
a -            alternating sum
a *            product over variable
a T            tabulate expression over range → vector
a r            rewrite formula using rules
```

**Rewrite examples:**
```
a r a*b + a*c := a*(b+c)
a r sin(x)^2 := 1-cos(x)^2
a r cos(n pi) := 1 :: integer(n) :: n%2 = 0
a r [f(0) := 1, f(n) := n f(n-1) :: n > 0]
```
Put rules in `EvalRules` to apply automatically, or in `AlgSimpRules` to apply during `a s`.

## 22. Display and Formatting

```
p              set floating-point precision (prompts, or prefix arg)
d r            display in arbitrary radix (prompts for base 2–36)
d z            toggle leading zeros
d f            fixed-point format (prompts for decimal places)
d s            scientific notation format
d e            engineering notation (exponent multiple of 3)
d n            normal float format (default)
d ,            toggle digit grouping (e.g. 1,000,000)
d g            set grouping size
d l            toggle line numbers on/off
d B            "Big" display mode (2D rendered formulas)
d N            Normal language mode (default)
d U            Unformatted mode
d c            toggle rectangular/polar display of complex numbers
d i            toggle i/j notation for complex numbers
d "            toggle string display (vectors of integers as quoted strings)
t d            toggle trail display on/off
m f            toggle Fraction mode (results as fractions instead of floats)
m s            toggle Symbolic mode (leave sqrt(2) unevaluated, etc.)
m i            toggle Infinite mode (allow inf in results)
m O            suppress evaluation of formulas
m D            return to default evaluation rules
m a            set mode where algebraic entry used by default
m m            record mode settings permanently
```

## 23. Strings

```
"              enter a string (stored as vector of ASCII codes)
```

Strings are vectors of integers (0–255). Use vector operations for manipulation: `v l` (length), `v r` (char at index), `|` (concatenation), `v v` (reverse), etc.

---

## 24. Common Idioms

### Number of digits
```
H L F 1 +
```
Computes `1 + floor(log10(n))`. Consumes n.

### First m digits of n
```
TAB RET H L F 1 + C-u 3 C-M-i - n f S F
```
Stack input: `2: n  1: m`. Consumes both.

### Last m digits of n
```
10 TAB ^ %
```
Stack input: `2: n  1: m`. Consumes both.

### Sum of digits
```
0 TAB Z{ RET 10 % RET C-u 4 C-M-i + C-u 3 TAB - RET 0 a= Z/ 10 \ Z} DEL
```
Consumes n, leaves the digit sum.

### Product of digits
```
1 TAB Z{ RET 10 % RET C-u 4 C-M-i * C-u 3 TAB - RET 0 a= Z/ 10 \ Z} DEL
```
Consumes n, leaves the digit product.

### Digit list (as vector)
```
[] TAB Z{ RET 10 % RET C-u 4 C-M-i v k C-u 3 TAB - RET 0 a= Z/ 10 \ Z} DEL
```
Consumes n, leaves `[d1, d2, ..., dk]` (most significant first).

### Reverse number
```
0 TAB Z{ RET 0 a= Z/ RET 10 \ TAB 10 % C-u 3 C-M-i 10 * + TAB Z} DEL
```
Consumes n, leaves the reversed number.

### Palindrome check
```
[] TAB Z{ RET 10 % RET C-u 4 C-M-i v k C-u 3 TAB - RET 0 a= Z/ 10 \ Z} DEL RET v v a=
```
Consumes n, leaves 1 if palindromic, 0 otherwise.

### Divisor count (via prime factorization, fast)
For n >= 4. Uses the formula: if `n = p1^a1 * ... * pr^ar`, then `d(n) = (1+a1) * ... * (1+ar)`.
```
k f 1 SPC TAB 0 SPC TAB 0 SPC TAB RET v l 1 SPC TAB Z( C-j TAB ~ v r RET C-u 4 C-j a= Z[ DEL C-u 3 C-M-i 1 + C-u 3 TAB Z: C-u 4 C-M-i 1 + C-u 5 C-M-i * C-u 4 TAB 1 SPC C-u 4 TAB C-u 3 M-DEL TAB Z] 1 Z) DEL DEL 1 + *
```

### Generic "for all digits" template
```
'acc_initial TAB Z{ RET 10 % RET C-u 4 C-M-i
   ;; Stack:
   ;;   2: accumulator
   ;;   1: current digit
   ;; === do something with digit (must consume it) ===
C-u 3 TAB - RET 0 a= Z/ 10 \ Z} DEL
```

---

## Execution

Copy a macro into GNU Emacs, select it, run `M-x read-kbd-macro`, then go to Calc and press `X`.

Or use the Python test harness: `python3 -c "from src.runner import CalcRunner; r = CalcRunner(); print(r.run_macro('...'))"`.
