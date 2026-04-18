from pathlib import Path


def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    lines = data.splitlines()

    for line in lines:
        information = line.split(", ")
        N, H = int(information[0]), int(information[1])
        print(min_num_of_drops(N, H))

def min_num_of_drops(N: int, H: int) -> int:
    dp = [0] * (N + 1)
    drops = 0

    while dp[N] < H:
        drops += 1
        for i in range(N, 0, -1):
            dp[i] = dp[i] + dp[i - 1] + 1

    return drops


if __name__ == "__main__":
    main()
