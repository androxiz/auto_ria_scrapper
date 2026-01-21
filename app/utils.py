import re

def parse_int(text: str | None) -> int | None:
    if not text:
        return 0

    cleaned = re.sub(r"[^\d\s]", "", text)
    nums = re.findall(r"\d+", cleaned)
    if not nums:
        return 0
    return int("".join(nums))


def parse_odometer(text: str | None) -> int | None:
    if not text:
        return 0

    t = text.lower().replace(" ", "")
    match_thousand = re.search(r"(\d+)(?:тис|т)", t)
    if match_thousand:
        return int(match_thousand.group(1)) * 1000

    nums = re.findall(r"\d+", t)
    return int("".join(nums)) if nums else 0


def parse_phone(text: str | None) -> str:
    if not text:
        return "Unknown"

    cleaned = re.sub(r"[^\d\(\)\+\-]", "", text)
    return cleaned if cleaned else "Unknown"