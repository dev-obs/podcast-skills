"""Compare Auphonic and reviewed or round-tripped WebVTT cues."""

import argparse
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from html import unescape
from pathlib import Path
import re


TIMESTAMP = r"(?:[0-9]{2,}:)?[0-5][0-9]:[0-5][0-9]\.[0-9]{3}"
TIMING_LINE = re.compile(
    rf"(?P<start>{TIMESTAMP})[ \t]+-->[ \t]+(?P<end>{TIMESTAMP})"
    r"(?:[ \t]+(?P<settings>.*))?"
)
VOICE_TAG = re.compile(r"<v(?:\.[^<>\s.]+)*[ \t]+([^<>]+)>")


@dataclass(frozen=True)
class Cue:
    start: Decimal
    end: Decimal
    settings: tuple
    speakers: tuple
    payload: str


def seconds(timestamp):
    minutes, remainder = timestamp.rsplit(":", 1)
    hours, _, minutes = minutes.rpartition(":")
    return int(hours or 0) * 3600 + int(minutes) * 60 + Decimal(remainder)


def read_cues(path, duration):
    # utf-8-sig accepts the optional BOM and read_text normalizes line endings.
    text = path.read_text(encoding="utf-8-sig").rstrip("\n")
    header, *blocks = re.split(r"\n(?:[ \t]*\n)+", text)
    if not re.fullmatch(r"WEBVTT(?:[ \t][^\n]*)?", header.split("\n", 1)[0]):
        raise ValueError(f"{path}: missing WEBVTT header")

    cues = []
    for block in blocks:
        lines = block.splitlines()
        first = lines[0]
        if first in {"STYLE", "REGION"} or re.match(r"NOTE(?:[ \t]|$)", first):
            continue
        timing_index = 0 if "-->" in first else 1
        timing_line = lines[timing_index] if len(lines) > timing_index else ""
        timing = TIMING_LINE.fullmatch(timing_line.strip())
        cue_number = len(cues) + 1
        if timing is None:
            raise ValueError(f"{path}: cue {cue_number} has invalid timing")

        start, end = (seconds(timing[field]) for field in ("start", "end"))
        if start >= end or (cues and start < cues[-1].start):
            raise ValueError(f"{path}: cue {cue_number} has an invalid time range")
        if duration is not None and end > duration:
            raise ValueError(f"{path}: cue {cue_number} ends beyond the master ({end}s)")

        payload = "\n".join(lines[timing_index + 1 :])
        if not payload.strip():
            raise ValueError(f"{path}: cue {cue_number} has no text")
        speakers = tuple(unescape(name).strip() for name in VOICE_TAG.findall(payload))
        settings = tuple((timing["settings"] or "").split())
        # The host may round-trip HTML entities differently in exported cue text.
        cues.append(Cue(start, end, settings, speakers, unescape(payload)))

    if not cues:
        raise ValueError(f"{path}: no cues found")
    return cues


def verify(original, candidate, match_text):
    if len(original) != len(candidate):
        raise ValueError(f"cue count changed ({len(original)} to {len(candidate)})")

    fields = ["start", "end", "settings", "speakers"]
    if match_text:
        fields.append("payload")
    for number, (before, after) in enumerate(zip(original, candidate), 1):
        changed = [field for field in fields if getattr(before, field) != getattr(after, field)]
        if changed:
            raise ValueError(f"cue {number} changed: {', '.join(changed)}")


def parse_duration(value):
    try:
        duration = Decimal(value)
    except InvalidOperation as error:
        raise argparse.ArgumentTypeError("expected a positive duration in seconds") from error
    if not duration.is_finite() or duration <= 0:
        raise argparse.ArgumentTypeError("expected a positive duration in seconds")
    return duration


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--duration", type=parse_duration, help="final audio duration in seconds")
    parser.add_argument("--match-text", action="store_true", help="also compare reviewed cue text")
    args = parser.parse_args()

    try:
        original = read_cues(args.original, args.duration)
        candidate = read_cues(args.candidate, args.duration)
        verify(original, candidate, args.match_text)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")

    text_result = " and text" if args.match_text else ""
    print(f"Verified {len(original)} cues: timing, settings, speaker labels{text_result}.")


if __name__ == "__main__":
    main()
