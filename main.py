#!/usr/bin/env python3
"""Write the competition entry image to /output/entry.png (1024x1024 PNG shipped in this repo); stdlib only, no network, deterministic."""
import os
import shutil

def main():
    # Determine output directory: MAKEFUN_OUTPUT_DIR env var, ./output, or /output
    # Prefer /output if it exists, otherwise use MAKEFUN_OUTPUT_DIR or ./output
    if os.path.isdir("/output"):
        output_dir = "/output"
    else:
        output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "./output")
    os.makedirs(output_dir, exist_ok=True)

    # Copy entry.png to output directory
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(output_dir, "entry.png")
    shutil.copy2(src, dst)
    print(dst)

if __name__ == "__main__":
    main()
