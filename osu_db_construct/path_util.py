import os
import platform
from pathlib import Path


def canonical_path(path):
    return Path(os.path.expandvars(str(path))).expanduser().resolve().absolute()


def get_osu_dir():
    system_defaults = {
        "Windows": "%localappdata%/osu!",
        "Darwin": "/Applications/osu!.app/Contents/Resources/drive_c/Program Files/osu!/"
    }
    d = system_defaults.get(platform.system(), None)
    if d:
        d = canonical_path(d)
        if d.is_dir():
            return d
    return canonical_path(input("Enter osu! directory: "))


def replace_invalid_filename(name, replacement="_"):
    invalid = '<>:"/\\|?*' + "".join(chr(i) for i in range(32))
    for c in invalid:
        name = name.replace(c, replacement)
    return name
