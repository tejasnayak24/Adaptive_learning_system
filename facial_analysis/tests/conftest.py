import sys
from pathlib import Path

FACIAL_DIR = Path(__file__).resolve().parents[1]
TESTS_DIR = Path(__file__).resolve().parent

for path in (FACIAL_DIR, TESTS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
