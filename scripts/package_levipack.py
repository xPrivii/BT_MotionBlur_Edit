#!/usr/bin/env python3
import argparse
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    library = args.library.resolve()
    output = args.output.resolve()
    if not library.is_file():
        raise SystemExit(f"Native library not found: {library}")
    if library.name != "libMotionBlur.so":
        raise SystemExit("Expected output library named libMotionBlur.so")

    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(library, output.parent / "libMotionBlur.so")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as pack:
        pack.write(ROOT / "manifest.json", "manifest.json")
        pack.write(library, "libMotionBlur.so")
        pack.write(ROOT / "config/config.json", "config/config.json")

    with zipfile.ZipFile(output) as pack:
        names = set(pack.namelist())
        required = {"manifest.json", "libMotionBlur.so", "config/config.json"}
        if names != required:
            raise RuntimeError(f"Unexpected package contents: {sorted(names)}")
        packed_manifest = json.loads(pack.read("manifest.json"))
        if packed_manifest != manifest or packed_manifest["entry"] != "libMotionBlur.so":
            raise RuntimeError("Manifest validation failed")
        if pack.getinfo("libMotionBlur.so").file_size != library.stat().st_size:
            raise RuntimeError("Library size mismatch")
    print(f"Created {output}")

if __name__ == "__main__":
    main()
