from pathlib import Path
import json


def clean_key(key):
    key = key.replace(".", "")
    key = key.strip().lower()
    key = key.replace(" ", "_")
    key = key.replace("-", "_")
    return key


def clean_value(value):
    value = value.replace("(Preferred)", "")
    value = value.replace("(Deprecated)", "")
    value = value.replace("(Deferred)", "")
    return value.strip()


def parse_line_to_key_value(line: str):
    if ":" not in line:
        return None, line.strip()
    left, right = line.split(":", 1)
    key = clean_key(left)
    value = right.strip()
    return key, value


def parse_ipconfig(lines):
    adapters = []
    configs = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].strip()

        if line == "":
            i += 1
            continue

        if line.lower().endswith("configuration"):
            i, data = handle_configuration_block(lines, i, n)
            configs.append(data)
            continue

        if "adapter" in line.lower():
            i, data = handle_adapter_block(lines, i, n)
            adapters.append(data)
            continue

        i += 1

    return adapters, configs


def handle_configuration_block(lines, i, n):
    name = lines[i].strip()
    i += 2
    block, i = read_block(lines, i, n)
    data = {"configuration_name": name}
    data.update(parse_block(block))
    return i, data


def handle_adapter_block(lines, i, n):
    name = lines[i].strip()
    i += 2
    block, i = read_block(lines, i, n)

    parsed = parse_block(block)

    data = {"adapter_name": name.replace(":", "")}

    for key in allowed:
        if key in parsed:
            data[key] = parsed[key]
        else:
            if key in ("dns_servers", "default_gateway"):
                data[key] = []
            else:
                data[key] = ""

    return i, data






def read_block(lines, i, n):
    block = []
    while i < n and lines[i].strip() != "":
        block.append(lines[i])
        i += 1
    return block, i + 1


allowed = [
    "description",
    "physical_address",
    "dhcp_enabled",
    "ipv4_address",
    "subnet_mask",
    "default_gateway",
    "dns_servers"
]


def parse_block(lines):
    data = {}
    current_key = None

    for line in lines:
        stripped = line.strip()

        if is_key_value_line(stripped):
            current_key = process_key_value_line(stripped, data)
            continue

        if current_key:
            process_continuation_line(stripped, current_key, data)

    return data


def is_key_value_line(line):
    if ":" not in line:
        return False
    left = line.split(":", 1)[0]
    return " " in left


def process_key_value_line(line, data):
    left, right = line.split(":", 1)
    key = clean_key(left)
    value = clean_value(right)

    if key in ("dns_servers", "default_gateway"):
        data[key] = value.split() if value else []
    else:
        data[key] = value if value else ""

    return key


def process_continuation_line(stripped, current_key, data):
    stripped = clean_value(stripped)

    if current_key in ("dns_servers", "default_gateway"):
        if stripped:
            data[current_key].extend(stripped.split())
    else:
        data[current_key] += " " + stripped


def parse_file(path):
    try:
        text = path.read_text(encoding="utf-16")
    except UnicodeError:
        text = path.read_text(encoding="utf-8", errors="ignore")

    lines = text.splitlines()
    adapters, configs = parse_ipconfig(lines)

    return {
        "file_name": "ipconfig.log",
        "adapters": adapters,
    }


def write_output_json(result, filename="output.json"):
    Path(filename).write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    files = sorted(
        [p for p in Path(".").iterdir() if p.suffix.lower() in {".txt", ".log"}]
    )

    output = []

    for f in files:
        parsed = parse_file(f)
        output.append(parsed)

    write_output_json(output)

    print(json.dumps(output, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()