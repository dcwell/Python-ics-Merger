"""Allow running the package with ``python -m ics_merger``."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
