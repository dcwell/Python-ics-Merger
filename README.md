# 📅 ICS Event Merger

A simple Python tool to merge multiple `.ics` calendar files into one or more combined files — perfect for importing into Google Calendar without duplicates.

I made this because I use a booking system for certian appointments that gave me single `.ics` file downloads rather than connecting to a calender service directly. In order to bulk import events into Google Calender (because there is no way to mass drop ics files into GCal at this time...) I had to merge all the files into one, then GCal would do the bulk import.

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
python merge_ics.py <directory_path>
```

---

## 📁 Output

my_calendars/
├── calendar1.ics
├── calendar2.ics
├── merged_events_1.ics
├── merged_events_2.ics
├── seen_events.json