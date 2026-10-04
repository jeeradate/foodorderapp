from pathlib import Path


def current_dir() -> str:
    return str(Path(__file__).resolve().parents[1].as_posix())
