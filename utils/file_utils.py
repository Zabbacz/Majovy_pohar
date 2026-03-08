# utils/file_utils.py

import os
import sys
import subprocess


def open_pdf(path: str) -> None:
    """
    Otevře PDF v defaultním prohlížeči podle OS.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    if sys.platform.startswith("linux"):
        subprocess.Popen(["xdg-open", path])
    elif sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore
    elif sys.platform.startswith("darwin"):
        subprocess.Popen(["open", path])
    else:
        raise RuntimeError(f"Nepodporovaný OS: {sys.platform}")
