from pathlib import Path

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    lines = data.splitlines()

    for line in lines:
        print(next_magic_num(evaluate_expr(line)))

def next_magic_num(num_str: str) -> str:
    if all(c == '9' for c in num_str):
        return '1' + ('0' * (len(num_str) - 1)) + '1'

    n = len(num_str)
    half = n // 2

    if n % 2 == 0:
        left = num_str[:half]
        middle = ''
    else:
        left = num_str[:half]
        middle = num_str[half]

    if middle:
        candidate = left + middle + left[::-1]
    else:
        candidate = left + left[::-1]

    if candidate > num_str:
        return candidate

    if middle:
        center = left + middle
    else:
        center = left

    center_int = int(center) + 1
    center_str = str(center_int).zfill(len(center))

    if middle:
        new_left = center_str[:-1]
        new_middle = center_str[-1]
        return new_left + new_middle + new_left[::-1]
    else:
        new_left = center_str
        return new_left + new_left[::-1]
    
def evaluate_expr(expr: str) -> str:
    expr = expr.strip()
    if '^' in expr:
        parts = expr.split('^')
        
        base, exp = parts

        result = int(base) ** int(exp)
        return str(result)


    return expr

if __name__ == "__main__":
    main()