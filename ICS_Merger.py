"""Convenience launcher for running the ICS Event Merger without installing it.

This thin wrapper lets you run the tool straight from a clone:

    python ICS_Merger.py                 # open the drag-and-drop GUI
    python ICS_Merger.py <directory>     # merge every .ics file in <directory>

For an installed experience, run ``pip install .`` and use the ``ics-merger``
command or ``python -m ics_merger`` instead. All of the real logic lives in the
``ics_merger`` package under ``src/``.
"""

import os
import sys

# Make the src/ layout importable when running from a clone (no install needed).
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from ics_merger.cli import main  # noqa: E402  (import follows sys.path setup)

if __name__ == "__main__":
    sys.exit(main())