"""Core engine for merging .ics calendar files.

This module contains all of the merging logic: scanning a directory for
``.ics`` files, building duplicate-detection signatures, maintaining the
``seen_events.json`` cache, and writing the merged output in chunks of at most
``CHUNK_SIZE`` events per file.

The functions here are UI-agnostic so they can be driven by either the
command-line entry point or the drag-and-drop GUI.
"""

import os
import json
from icalendar import Calendar

CHUNK_SIZE = 500  # events per file

def normalize_event(event):
    """Build a hashable signature that uniquely identifies an event.

    The signature combines the event's UID, start, end, and summary so that
    duplicate events across files can be detected reliably.

    Args:
        event: An icalendar VEVENT component.

    Returns:
        A tuple of (UID, DTSTART, DTEND, SUMMARY) as strings.
    """
    return (
        str(event.get('UID')),
        str(event.get('DTSTART')),
        str(event.get('DTEND')),
        str(event.get('SUMMARY')),
    )

def get_ics_files(directory):
    """Return the full paths of all .ics files in a directory.

    Args:
        directory: Path to the directory to scan.

    Returns:
        A list of absolute paths to files ending in ``.ics`` (case-insensitive).
    """
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith('.ics')
    ]

def get_cache_path(directory):
    """Return the path to the deduplication cache file for a directory.

    Args:
        directory: Path to the working directory.

    Returns:
        The path to ``seen_events.json`` inside ``directory``.
    """
    return os.path.join(directory, "seen_events.json")

def load_seen(directory):
    """Load the set of previously processed event signatures.

    Args:
        directory: Path to the directory containing the cache file.

    Returns:
        A set of event signature tuples. Returns an empty set if no cache
        file exists yet.
    """
    cache_file = get_cache_path(directory)
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return set(tuple(x) for x in json.load(f))
    return set()

def save_seen(directory, seen):
    """Persist the set of processed event signatures to the cache file.

    Args:
        directory: Path to the directory where the cache should be written.
        seen: A set of event signature tuples to store.
    """
    cache_file = get_cache_path(directory)
    with open(cache_file, "w") as f:
        json.dump(list(seen), f)

def write_chunk(events, index, directory):
    """Write a batch of events to a numbered merged .ics file.

    Args:
        events: A list of icalendar VEVENT components to write.
        index: The chunk number used in the output filename.
        directory: Path to the directory where the file is saved.
    """
    cal = Calendar()
    cal.add('prodid', '-//ICS Merge Tool//')
    cal.add('version', '2.0')

    for e in events:
        cal.add_component(e)

    filename = os.path.join(directory, f"merged_events_{index}.ics")

    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

    print(f"Created {filename} with {len(events)} events")

def merge_ics_files(files, output_dir):
    """Merge a list of .ics files into deduplicated output files.

    Collects new (unseen) events from every file in ``files`` and writes them
    out in chunks of up to ``CHUNK_SIZE`` events per file. Already-processed
    events are skipped using the ``seen_events.json`` cache in ``output_dir``,
    which is updated at the end so future runs remain duplicate-safe.

    Args:
        files: Iterable of paths to .ics files to merge.
        output_dir: Directory where ``merged_events_*.ics`` files and the
            ``seen_events.json`` cache are written.

    Returns:
        The number of new (non-duplicate) events that were added.
    """
    seen = load_seen(output_dir)
    chunk = []
    chunk_index = 1
    total_added = 0

    for file in files:
        with open(file, 'rb') as f:
            cal = Calendar.from_ical(f.read())

            for component in cal.walk():
                if component.name == "VEVENT":
                    sig = normalize_event(component)

                    if sig in seen:
                        continue

                    seen.add(sig)
                    chunk.append(component)
                    total_added += 1

                    if len(chunk) >= CHUNK_SIZE:
                        write_chunk(chunk, chunk_index, output_dir)
                        chunk = []
                        chunk_index += 1

    if chunk:
        write_chunk(chunk, chunk_index, output_dir)

    save_seen(output_dir, seen)
    return total_added

def merge_ics_from_directory(directory):
    """Merge all .ics files in a directory into deduplicated output files.

    Scans ``directory`` for source files and writes the merged output and the
    ``seen_events.json`` cache back into the same directory.

    Args:
        directory: Path to the directory containing the source .ics files.
            Output files and the cache are written to this same directory.
    """
    files = get_ics_files(directory)

    if not files:
        print("No .ics files found.")
        return

    total_added = merge_ics_files(files, directory)

    print(f"\n✅ Added {total_added} new events")
    print(f"✅ Files saved to: {directory}")
    print("✅ Duplicate-safe for future runs")
