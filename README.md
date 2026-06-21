# 📅 ICS Event Merger

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.x-blue)

A simple Python tool to merge multiple `.ics` calendar files into one or more combined files — perfect for importing into Google Calendar without duplicates.

I made this because I use a booking system for certain appointments that gave me single `.ics` file downloads rather than connecting to a calendar service directly. In order to bulk import events into Google Calendar (because there is no way to mass drop `.ics` files into GCal at this time...) I had to merge all the files into one, then GCal would do the bulk import.

---

## ✅ Features

- 📂 Merge all `.ics` files from a directory
- 🧠 Smart deduplication (prevents duplicate events)
- 🔁 Safe to re-run (remembers already processed events)
- 📦 Automatically splits large outputs into smaller files
- 📍 Saves output directly to your input directory

---

## 📦 Requirements

- Python 3.x
- `icalendar` library

Install dependencies:

```bash
pip install icalendar
```

---

## 🚀 Usage

```bash
python ICS_Merger.py <directory_path>
```

---

## 📁 Output

Merged files and the dedup cache are written **into the same input directory**:

```text
my_calendars/
├── calendar1.ics          # your original files (left untouched)
├── calendar2.ics
├── merged_events_1.ics    # combined output (up to 500 events each)
├── merged_events_2.ics
└── seen_events.json       # cache of processed events (enables safe re-runs)
```

---

## 🧠 How It Works

1. Every `.ics` file in the directory is scanned for events (`VEVENT`).
2. Each event gets a signature built from its **UID, start, end, and summary**.
3. Signatures are checked against `seen_events.json`; duplicates are skipped.
4. New events are written to `merged_events_*.ics` files, split into chunks of
   up to **500 events** (configurable via `CHUNK_SIZE` in the script).
5. The cache is updated so re-running never re-adds the same events.

> 💡 To force a clean re-merge, delete `seen_events.json` and the generated
> `merged_events_*.ics` files, then run the tool again.

---

## 📥 Importing into Google Calendar

1. Open [Google Calendar](https://calendar.google.com) on the web.
2. Go to **Settings ⚙️ → Import & Export**.
3. Under **Import**, select a `merged_events_*.ics` file.
4. Choose the destination calendar and click **Import**.
5. Repeat for each `merged_events_*.ics` file if more than one was created.

---

## 📝 Notes

- Your original `.ics` files are never modified or deleted.
- Output and the cache are saved directly to the input directory.
- Adjust `CHUNK_SIZE` in `ICS_Merger.py` to change events-per-file.

---

## 🏷️ Versioning

This project follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`):

- **MAJOR** — incompatible or breaking changes
- **MINOR** — new features, backward compatible
- **PATCH** — bug fixes, backward compatible

The current version is shown in the badge at the top of this README. When releasing
a new version, add a row to the changelog below, bump the badge number, and tag the
release on GitHub:

```bash
git tag -a v1.0.0 -m "v1.0.0"
git push origin v1.0.0
```

> 💡 Pushing a tag lets you publish a matching **GitHub Release**, which then
> appears automatically under the repository's **Releases** section.

### 📜 Changelog

| Version | Date       | Changes                                                            |
| ------- | ---------- | ------------------------------------------------------------------ |
| 1.0.0   | 2026-06-21 | Initial release: directory merge, dedup cache, and chunked output. |
