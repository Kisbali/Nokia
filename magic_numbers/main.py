from pathlib import Path

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    lines = data.splitlines()

    for line in lines:
        print(next_magic_num(evaluate_expr(line)))

def next_magic_num(num_str: str) -> str:
    if all(c == '9' for c in num_str):
        return '1' + ('0' * (len(num_str) - 1)) + '1'

    left, middle = split_number(num_str)

    candidate = build_palindrome(left, middle)
    if candidate > num_str:
        return candidate

    base = left + middle
    base = increment_base(base)

    if middle:
        new_left, new_middle = base[:-1], base[-1]
        return build_palindrome(new_left, new_middle)
    return build_palindrome(base, '')

def build_palindrome(left: str, middle: str) -> str:
    if middle:
        return left + middle + left[::-1]
    return left + left[::-1]

def increment_base(base: str) -> str:
    return str(int(base) + 1).zfill(len(base))

def split_number(num_str: str) -> tuple[str, str]:
    n = len(num_str)
    half = n // 2

    if n % 2 == 0:
        return num_str[:half], ''
    return num_str[:half], num_str[half]

def evaluate_expr(expr: str) -> str:
    expr = expr.strip()
    if '^' in expr:
        parts = expr.split('^')

        if len(parts) != 2:
            raise ValueError(expr)
        
        base, exp = parts

        result = int(base) ** int(exp)
        return str(result)
    return expr

if __name__ == "__main__":
    main()