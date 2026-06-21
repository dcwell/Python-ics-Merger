import os
import sys
import json
from icalendar import Calendar

CHUNK_SIZE = 500  # events per file

def normalize_event(event):
    return (
        str(event.get('UID')),
        str(event.get('DTSTART')),
        str(event.get('DTEND')),
        str(event.get('SUMMARY')),
    )

def get_ics_files(directory):
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith('.ics')
    ]

def get_cache_path(directory):
    return os.path.join(directory, "seen_events.json")

def load_seen(directory):
    cache_file = get_cache_path(directory)
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return set(tuple(x) for x in json.load(f))
    return set()

def save_seen(directory, seen):
    cache_file = get_cache_path(directory)
    with open(cache_file, "w") as f:
        json.dump(list(seen), f)

def write_chunk(events, index, directory):
    cal = Calendar()
    cal.add('prodid', '-//ICS Merge Tool//')
    cal.add('version', '2.0')

    for e in events:
        cal.add_component(e)

    filename = os.path.join(directory, f"merged_events_{index}.ics")

    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

    print(f"Created {filename} with {len(events)} events")

def merge_ics_from_directory(directory):
    files = get_ics_files(directory)

    if not files:
        print("No .ics files found.")
        return

    seen = load_seen(directory)
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
                        write_chunk(chunk, chunk_index, directory)
                        chunk = []
                        chunk_index += 1

    if chunk:
        write_chunk(chunk, chunk_index, directory)

    save_seen(directory, seen)

    print(f"\n✅ Added {total_added} new events")
    print(f"✅ Files saved to: {directory}")
    print(f"✅ Duplicate-safe for future runs")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python merge_ics.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print("Invalid directory.")
        sys.exit(1)

    merge_ics_from_directory(directory)