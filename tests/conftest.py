import sys
from pathlib import Path

# The package and the flat modules (pulse_quantities.py etc.) are in src/. Make them importable for the tests regardless of
# where pytest is invoked from, and of which copy of goldpan the environment has installed.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
