"""Entry-point logic for the ICS Event Merger.

Exposes :func:`main`, which powers the ``ics-merger`` console script, the
``python -m ics_merger`` module runner, and the root ``ICS_Merger.py`` launcher.
"""

import os
import sys

from .merger import merge_ics_from_directory
from .gui import run_gui


def main(argv=None):
    """Run the merger from the command line or open the GUI.

    With a directory argument, every ``.ics`` file inside it is merged from the
    command line. With no arguments, the drag-and-drop GUI is launched instead.

    Args:
        argv: Optional list of arguments (defaults to ``sys.argv[1:]``).

    Returns:
        A process exit code: ``0`` on success, ``1`` on invalid input.
    """
    args = sys.argv[1:] if argv is None else list(argv)

    if args:
        directory = args[0]
        if not os.path.isdir(directory):
            print("Invalid directory.")
            return 1
        merge_ics_from_directory(directory)
        return 0

    run_gui()
    return 0
