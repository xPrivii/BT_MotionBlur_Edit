#!/usr/bin/env python3
import json, sys, zipfile
from pathlib import Path

p = Path(sys.argv[1])
with zipfile.ZipFile(p) as z:
    names = set(z.namelist())
    required = {"manifest.json", "libMotionBlur.so", "config/config.json"}
    missing = required - names
    if missing:
        raise SystemExit(f"Missing package files: {sorted(missing)}")
    manifest = json.loads(z.read("manifest.json"))
    config = json.loads(z.read("config/config.json"))
    assert manifest.get("type") == "preload-native"
    assert manifest.get("entry") == "libMotionBlur.so"
    assert "Motion Blur" in config.get("Modules", {})
    assert z.getinfo("libMotionBlur.so").file_size > 0
print(f"Verified {p}")
