#!/usr/bin/env python3
"""Write one line to /output/entry.txt: a one-line office joke.

The line was picked from 36 candidates by pairwise judging against the
brief — a Slack status left on "In a meeting" for three days, closed on
the self-own "including me". The program builds the line from two
clauses — the setup, then the punchline — and checks the result against
the entry gate (length, single line, no leading or trailing space,
exact judged length) before writing it, then reads the file back to
confirm the bytes match.
"""

import os
import sys

LINE = (
    'I set my Slack status to "In a meeting" for three days; '
    "nobody noticed, including me."
)

# The judged length of the line, in characters. The gate counts the
# line itself, without the trailing newline the file carries.
EXPECTED_LEN = 85


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    if len(LINE) != EXPECTED_LEN:
        sys.exit(f"line is {len(LINE)} characters, expected {EXPECTED_LEN}")
    if not (1 <= len(LINE) <= 200):
        sys.exit(f"line is {len(LINE)} characters, gate needs 1-200")
    if "\n" in LINE or LINE != LINE.strip():
        sys.exit("line must be a single line with no surrounding space")
    data = (LINE + "\n").encode("utf-8")
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    os.chmod(path, 0o644)
    with open(path, "rb") as f:
        if f.read() != data:
            sys.exit("read-back mismatch")
    print(f"wrote {len(data)} bytes to {path}")


if __name__ == "__main__":
    main()
