# Examples of annotated and compact macros:


## Example 1

**Annotated macro:**
```
600851475143      ;; 1: 600851475143
k f               ;; 1: [71, 839, 1471, 6857]
v v               ;; 1: [6857, 1471, 839, 71]   (reversed)
v r 1 RET         ;; 1: 6857                     (first element)
```

**Compact macro:**
```
600851475143 k f v v v r 1 RET
```

## Example 2

**Annotated macro:**
```
v x 20 RET    ;; 1: [1, 2, 3, ..., 20]     (iota)
v R k l       ;; 1: 232792560               (reduce with LCM)
```

**Compact macro:**
```
v x 20 RET v R k l
```


## Example 3

**Annotated macro:**
```
0 SPC 1 SPC 100    ;; 3: 0   2: 1   1: 100    (accumulator, lo, hi)
Z(                  ;; for i = 1 to 100:
   +                ;;   accumulator += i
1 Z)                ;;   step = 1
RET *               ;; 1: (sum)^2              (square the sum)
0 SPC 1 SPC 100    ;; 3: (sum)^2  2: 0  1: ...
Z(                  ;; for i = 1 to 100:
   RET * +          ;;   accumulator += i*i     (dup i, square, add to acc)
1 Z)                ;;   step = 1
-                   ;; 1: (sum)^2 - sum(k^2)
```

**Compact macro:**
```
0 SPC 1 SPC 100 Z( + 1 Z) RET * 0 SPC 1 SPC 100 Z( RET * + 1 Z) -
```

## Example 4

**Annotated macro:**
```
2 SPC               ;; 1: 2                    (first prime)
10001 SPC 1 -        ;; 2: 2  1: 10000
Z< k n Z>           ;; repeat 10000 times: next prime
```

**Compact macro:**
```
2 SPC 10001 SPC 1 - Z< k n Z>
```

## Example 5

**Annotated macro:**
```
0 SPC                         ;; 1: 0                    (running sum)
0 SPC                         ;; 2: 0  1: 0              (fib(n-1))
1                              ;; 3: 0  2: 0  1: 1       (fib(n))
Z{                             ;; repeat-until:
   TAB C-j +                  ;;   compute next Fibonacci (swap, copy prev, add)
   RET 4000000 TAB a< Z/      ;;   if fib > 4000000, break
   RET RET 2 % Z[             ;;   if fib is odd...
      DEL                     ;;     discard the test residue
   Z:                          ;;   else (fib is even)...
      C-u 4 C-M-i + C-u 3 TAB ;;     add fib to running sum (element #4)
   Z]
Z}                             ;; end repeat
DEL DEL                       ;; delete remaining Fibonacci numbers
```

**Compact macro:**
```
0 SPC 0 SPC 1 Z{ TAB C-j + RET 4000000 TAB a< Z/ RET RET 2 % Z[ DEL Z: C-u 4 C-M-i + C-u 3 TAB Z] Z} DEL DEL
```

**Expected result:** 4613732
**Features:** `Z{ ... Z/ ... Z}` (repeat-until with break), `Z[ ... Z: ... Z]` (if-else)

---

## Example 6

**Annotated macro:**
```
2 SPC 1000 ^       ;; 1: 2^1000                    (a 302-digit number)
;; digit sum idiom:
0 TAB               ;; 2: 0 (accumulator)  1: 2^1000
Z{                  ;; repeat-until:
   RET 10 %        ;;   2: n  1: last digit
   RET              ;;   3: n  2: digit  1: digit
   C-u 4 C-M-i     ;;   rotate acc from #4 to #1
   + C-u 3 TAB     ;;   add digit to acc, rotate back
   - RET 0 a= Z/   ;;   subtract digit from n; if n=0, break
   10 \             ;;   integer-divide by 10
Z} DEL              ;; drop leftover
```

**Compact macro:**
```
2 SPC 1000 ^ 0 TAB Z{ RET 10 % RET C-u 4 C-M-i + C-u 3 TAB - RET 0 a= Z/ 10 \ Z} DEL
```

## Example 7

**Annotated macro:**
```
100 !               ;; 1: 100!                   (a 158-digit number)
;; digit sum idiom:
0 TAB Z{ RET 10 % RET C-u 4 C-M-i + C-u 3 TAB - RET 0 a= Z/ 10 \ Z} DEL
```

**Compact macro:**
```
100 ! 0 TAB Z{ RET 10 % RET C-u 4 C-M-i + C-u 3 TAB - RET 0 a= Z/ 10 \ Z} DEL
```

## Example 8

**Annotated macro:**
```
2 S-M 10000000000 SPC   ;; 1: 2 mod 10000000000     (modulo form)
7830457 ^                ;; 1: 2^7830457 mod 10^10    (modular exponentiation)
28433 *                  ;; 1: 28433 * 2^7830457 mod 10^10
1 +                      ;; 1: 28433 * 2^7830457 + 1 mod 10^10
v u DEL                  ;; unpack modulo form, discard modulus → 1: 8739992577
```

**Compact macro:**
```
2 S-M 10000000000 SPC 7830457 ^ 28433 * 1 + v u DEL
```

**Expected result:** 8739992577
**Features:** `S-M` (modulo form entry), modular exponentiation

