from pathlib import Path
from datetime import datetime
import math


def parse_datetime(dt: str) -> datetime:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(dt, fmt)
        except ValueError:
            pass
    raise ValueError("Hibás dátumformátum! Használd: YYYY-MM-DD HH:MM[:SS]")


def fee_under_24_minutes(total_minutes: int) -> int:
    if total_minutes <= 30:
        return 0
    remaining = total_minutes - 30
    fee = 0
    first_period = min(remaining, 180)
    first_hours = math.ceil(first_period / 60)
    fee += first_hours * 300
    if remaining > 180:
        extra = remaining - 180
        extra_hours = math.ceil(extra / 60)
        fee += extra_hours * 500
    return fee


def calculate_parking_fee(entry_time: str, exit_time: str) -> int:
    start = parse_datetime(entry_time)
    end = parse_datetime(exit_time)
    if end < start:
        raise ValueError("A kilépési idő nem lehet korábbi, mint a belépési idő!")
    total_minutes = math.ceil((end - start).total_seconds() / 60)
    if total_minutes <= 24 * 60:
        return min(fee_under_24_minutes(total_minutes), 10000)
    full_days = total_minutes // (24 * 60)
    remainder = total_minutes % (24 * 60)
    fee = full_days * 10000
    if remainder > 0:
        fee += min(fee_under_24_minutes(remainder), 10000)
    return fee


def process_line(line: str) -> str | None:
    line = line.strip()
    if not line or line.startswith("=") or line.startswith("RENDSZAM"):
        return None
    try:
        parts = line.split()
        plate = parts[0]
        entry = parts[1] + " " + parts[2]
        exit_ = parts[3] + " " + parts[4]
        fee = calculate_parking_fee(entry, exit_)
        return f"{plate}\t\t{fee}"
    except Exception as e:
        return f"Hiba a sor feldolgozásakor: {line}  ({e})"


def process_file(input_path: str) -> list[str]:
    data = Path(input_path).read_text(encoding="utf-8")
    lines = data.splitlines()
    results = []
    for line in lines:
        result = process_line(line)
        if result:
            results.append(result)
    return results


def main():
    output_lines = process_file("input.txt")
    Path("dij.txt").write_text("\n".join(output_lines), encoding="utf-8")
    print("RENDSZÁM\tDÍJ")
    print("\n".join(output_lines))


if __name__ == "__main__":
    main()
