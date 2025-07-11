#!/usr/bin/env python3
"""
rename_data.py  –  Rename all Plotly HTML files in ./data
to PR07-file<N>.html, stripping patient/date info.
Usage
  python rename_data.py        # do it
  python rename_data.py --dry  # show what *would* happen
"""

import argparse
from pathlib import Path

def main(dry: bool = False) -> None:
    data_dir = Path("data")
    if not data_dir.is_dir():
        raise SystemExit("❌  ./data folder not found")

    html_files = sorted(data_dir.glob("*.html"))
    if not html_files:
        raise SystemExit("❌  No .html files found in ./data")

    for idx, old_path in enumerate(html_files, start=1):
        new_name = f"PR07-file{idx:03d}.html"
        new_path = old_path.with_name(new_name)
        if dry:
            print(f"[dry-run] {old_path.name}  →  {new_name}")
        else:
            print(f"renaming {old_path.name}  →  {new_name}")
            old_path.rename(new_path)

    suffix = " (dry-run, nothing changed)" if dry else ""
    print(f"✔️  Completed{suffix}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch-rename Plotly HTML files")
    parser.add_argument("--dry", action="store_true", help="Preview without renaming")
    main(parser.parse_args().dry)
