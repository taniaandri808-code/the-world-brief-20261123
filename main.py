"""Write the competition entry image to /output/entry.png.

Simplest compliant program: the rendered 1024x1024 PNG ships with this
repository; main.py copies it to the output directory. Standard library only,
no network, deterministic (the same bytes every run).
"""
import os
import shutil


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")

    # The harness mounts /output; fall back to a local dir when run by hand.
    out_dir = "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = os.getenv("MAKEFUN_OUTPUT_DIR", os.path.join(here, "output"))
        os.makedirs(out_dir, exist_ok=True)

    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(dst)


if __name__ == "__main__":
    main()
