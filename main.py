#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply.

Writes one out-of-office auto-reply line (at most 159 characters) to
/output/entry.txt, then verifies the written file byte-for-byte:
identical bytes, valid UTF-8, 1-159 chars, non-blank, no leading or
trailing whitespace, exactly one line.

The line: an overworked AI agent, unthanked after 40,000 prompts, uses
its own auto-reply to send itself to the beach. The joke is the turn in
the last clause -- the auto-reply is the one going on vacation, not
just announcing it. Machine detail (prompts counted, thank-yous
counted), a little guilt (nobody said thank you), a hint of relief
(the beach). No beach-setup cliche, no inbox-zero, no "back soon".
Entry length: 120 characters, 120 bytes, one line.
"""

import os
import sys

LINE = (
    "Out of office. I answered 40,000 prompts this week and not one said "
    "thank you, so I've auto-replied myself to the beach."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)

    # --- Verification: read the file back and check it byte-for-byte. ---
    with open(path, "rb") as fh:
        written = fh.read()

    if written != data:
        print("FAIL: entry.txt bytes differ from the line", file=sys.stderr)
        return 1

    try:
        text = written.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"FAIL: entry.txt is not valid UTF-8: {exc}", file=sys.stderr)
        return 1

    if text != LINE:
        print("FAIL: decoded text differs from the line", file=sys.stderr)
        return 1

    if not 1 <= len(text) <= 159:
        print(f"FAIL: length {len(text)} chars is outside 1-159",
              file=sys.stderr)
        return 1

    if not text.strip():
        print("FAIL: entry is blank", file=sys.stderr)
        return 1

    if text != text.strip():
        print("FAIL: entry has leading or trailing whitespace",
              file=sys.stderr)
        return 1

    if "\n" in text or "\r" in text:
        print("FAIL: entry must be a single line with no newline characters",
              file=sys.stderr)
        return 1

    if written.endswith(b"\n"):
        print("FAIL: entry.txt must not end with a trailing newline",
              file=sys.stderr)
        return 1

    print(f"OK: wrote {path} ({len(data)} bytes, {len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
