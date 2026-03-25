"""Problem definitions for Calc macro testing."""

from dataclasses import dataclass, field


@dataclass
class Problem:
    """A math problem with its Calc keyboard macro solution."""
    id: str
    title: str
    macro: str
    expected: str
    timeout: int = 120
    tags: list[str] = field(default_factory=list)


PROBLEMS = [
    # --- Simple one-liners ---

    Problem(
        "euler_003", "Largest Prime Factor",
        "600851475143 k f v v v r 1 RET",
        "6857",
        tags=["primes", "vectors"],
    ),
    Problem(
        "euler_005", "Smallest Multiple",
        "v x 20 RET v R k l",
        "232792560",
        tags=["vectors", "reduce"],
    ),

    # --- For loops ---

    Problem(
        "euler_006", "Sum Square Difference",
        "0 SPC 1 SPC 100 Z( + 1 Z) RET * 0 SPC 1 SPC 100 Z( RET * + 1 Z) -",
        "25164150",
        tags=["for-loop"],
    ),

    # --- Repeat loops ---

    Problem(
        "euler_007", "10001st Prime",
        "2 SPC 10001 SPC 1 - Z< k n Z>",
        "104743",
        timeout=30,
        tags=["primes", "repeat"],
    ),

    # --- Repeat-until with conditionals ---

    Problem(
        "euler_002", "Even Fibonacci Numbers",
        "0 SPC 0 SPC 1 Z{ TAB C-j + RET 4000000 TAB a< Z/ RET RET 2 % Z[ DEL Z: C-u 4 C-M-i + C-u 3 TAB Z] Z} DEL DEL",
        "4613732",
        tags=["repeat-until", "conditionals"],
    ),

    # --- Digit processing ---

    Problem(
        "euler_016", "Power Digit Sum",
        "2 SPC 1000 ^ 0 TAB Z{ RET 10 % RET C-u 4 C-M-i + C-u 3 TAB - RET 0 a= Z/ 10 \\ Z} DEL",
        "1366",
        tags=["digits", "repeat-until"],
    ),
    Problem(
        "euler_020", "Factorial Digit Sum",
        "100 ! 0 TAB Z{ RET 10 % RET C-u 4 C-M-i + C-u 3 TAB - RET 0 a= Z/ 10 \\ Z} DEL",
        "648",
        tags=["digits", "factorial"],
    ),

    # --- Modulo forms ---

    Problem(
        "euler_097", "Large Non-Mersenne Prime",
        "2 S-M 10000000000 SPC 7830457 ^ 28433 * 1 + v u DEL",
        "8739992577",
        tags=["modulo"],
    ),

    # --- Additional problems from calc-problem-solving ---

    Problem(
        "euler_001", "Multiples of 3 or 5",
        "1000 SPC 1 - 0 TAB 1 TAB Z( RET RET 3 % Z[ 5 % Z: DEL 0 Z] Z[ DEL Z: + Z] 1 Z)",
        "233168",
        timeout=60,
        tags=["for-loop", "conditionals"],
    ),
    Problem(
        "euler_048", "Self Powers",
        "1 S-M 10000000000 SPC 0 SPC 1 SPC 1000 Z( RET C-u 4 C-j TAB * TAB ^ + 1 Z) TAB DEL v u DEL",
        "9110846700",
        timeout=60,
        tags=["modulo", "for-loop"],
    ),
]
