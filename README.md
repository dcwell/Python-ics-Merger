# 📅 ICS Event Merger

[![CI](https://github.com/dcwell/Python-ics-Merger/actions/workflows/ci.yml/badge.svg)](https://github.com/dcwell/Python-ics-Merger/actions/workflows/ci.yml)
![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A simple Python tool to merge multiple `.ics` calendar files into one or more combined files — perfect for importing into Google Calendar without duplicates.

I made this because I use a booking system for certain appointments that gave me single `.ics` file downloads rather than connecting to a calendar service directly. In order to bulk import events into Google Calendar (because there is no way to mass drop `.ics` files into GCal at this time...) I had to merge all the files into one, then GCal would do the bulk import.

---

## ✅ Features

- 🖱️ **Drag-and-drop GUI** — drop a pile of `.ics` files in and click merge
- 📂 Merge all `.ics` files from a directory (CLI)
- 🧠 Smart deduplication (prevents duplicate events)
- 🔁 Safe to re-run (remembers already processed events)
- 📦 Automatically splits large outputs into smaller files
- 📍 Saves output to the directory you choose

---

## 📦 Installation

> 🟢 **New to Python?** Just follow **Option A** below — copy each command into the
> **Terminal** app and press Enter, one line at a time. You don't need to know any
> Python to use this tool.

### Before you start

You need **Python 3.9 or newer**. Check what you have:

```bash
python3 --version
```

- If it prints something like `Python 3.12.4`, you're good to go.
- If it says *command not found*, install Python from
  [python.org/downloads](https://www.python.org/downloads/) (Mac users with
  [Homebrew](https://brew.sh) can run `brew install python` instead).

> 💻 **Opening the Terminal:** on macOS, press `Cmd + Space`, type `Terminal`, and press Enter.

### Option A — step by step (recommended)

These commands make a self-contained copy of the tool, so nothing else on your
computer is affected. Run them **one at a time, in order**:

```bash
# 1. Download the project and move into its folder
git clone https://github.com/dcwell/Python-ics-Merger.git
cd Python-ics-Merger

# 2. Create a "virtual environment" — a private sandbox for this tool's parts
python3 -m venv .venv

# 3. Turn the sandbox on  (you'll see "(.venv)" appear in your prompt)
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\Activate.ps1     # Windows (PowerShell)

# 4. Install the tool into the sandbox
pip install ".[gui]"
```

Done — the `ics-merger` command is now ready (jump to **Usage** below).

> 📦 **No `git`?** On the GitHub page, click the green **Code** button →
> **Download ZIP**, unzip it, then start from step 2 inside the unzipped folder.

> 🔁 **Coming back later?** In a new Terminal you don't reinstall — just `cd` back
> into the project folder and run `source .venv/bin/activate` again to switch the
> sandbox on. Run `deactivate` to switch it off; delete the `.venv` folder to
> remove everything.

> ⚠️ **Two things that trip people up:**
> - Keep the quotes: `pip install ".[gui]"` (some shells misread a bare `[ ]`).
> - Run it **inside the folder that contains `pyproject.toml`** — check with `ls pyproject.toml`.

### Option B — pipx (optional, more convenient long-term)

*Skip this if you already did Option A.* Once you're comfortable, [pipx](https://pipx.pypa.io/)
installs the `ics-merger` command so it works from any folder — no sandbox to switch
on each time:

```bash
cd Python-ics-Merger
pipx install ".[gui]"
```

### About the GUI extra

The `[gui]` extra pulls in [`tkinterdnd2`](https://pypi.org/project/tkinterdnd2/)
for true drag-and-drop; without it the GUI falls back to a native file picker.

> 🍎 Tkinter ships with most Python installs. On Homebrew Python you may need to
> add it — install the package matching your Python version, e.g.
> `brew install python-tk@3.14`.

---

## 🚀 Usage

### Step 1 — know your run command

What you type depends on how you installed it (from **Installation** above):

| If you installed with…        | …run the tool with    | Reminder                                          |
| ----------------------------- | --------------------- | ------------------------------------------------- |
| **Option A** — venv + pip     | `ics-merger`          | Activate the venv first: `source .venv/bin/activate` |
| **Option B** — pipx           | `ics-merger`          | Works from any folder                             |
| **No install** — from a clone | `python ICS_Merger.py`| Run from the project folder (dependencies must be installed) |

> `python -m ics_merger` is an equivalent alternative anywhere the package is installed.

### Step 2 — choose GUI or command line

The **argument** decides what happens — and it's the same for whichever command you picked above.

**🖥️ GUI (drag-and-drop)** — run it with **no argument**:

```bash
ics-merger
```

A window opens; drag `.ics` files (or whole folders) in, click **Merge ▶**, and pick
an output folder. (The GUI needs Tkinter — see Installation. Without `tkinterdnd2`
it falls back to a native file picker.)

**⌨️ Command line** — give it a **folder path**:

```bash
ics-merger /path/to/folder
```

Every `.ics` file in that folder is merged, with the output written to the same folder.

> Using the no-install launcher instead? Swap `ics-merger` for `python ICS_Merger.py`
> in the two examples above (e.g. `python ICS_Merger.py /path/to/folder`).

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

## 🗂️ Project Structure

```text
Python-ics-Merger/
├── ICS_Merger.py              # no-install launcher (delegates to the package)
├── pyproject.toml             # packaging, dependencies, console script, tooling
├── src/
│   └── ics_merger/
│       ├── __init__.py        # package metadata (__version__)
│       ├── __main__.py        # enables `python -m ics_merger`
│       ├── cli.py             # entry-point logic (main)
│       ├── merger.py          # core engine — scanning, dedup cache, chunking
│       └── gui.py             # drag-and-drop window (+ file-picker fallback)
├── tests/
│   └── test_merger.py         # pytest unit tests
├── .github/workflows/ci.yml   # CI: ruff lint + pytest matrix
├── LICENSE
└── README.md
```

---

## 🧠 How It Works

1. Every `.ics` file in the directory is scanned for events (`VEVENT`).
2. Each event gets a signature built from its **UID, start, end, and summary**.
3. Signatures are checked against `seen_events.json`; duplicates are skipped.
4. New events are written to `merged_events_*.ics` files, split into chunks of
   up to **500 events** (configurable via `CHUNK_SIZE` in `src/ics_merger/merger.py`).
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
- In CLI mode, output and the cache go to the input directory; in GUI mode you pick the output folder.
- Adjust `CHUNK_SIZE` in `src/ics_merger/merger.py` to change events-per-file.

---

## 🛠️ Troubleshooting

**`ModuleNotFoundError: No module named 'icalendar'`**
Your virtual environment isn't active (or your editor is running a different
Python). Activate it with `source .venv/bin/activate`, then confirm with
`which python` — the path should be inside `.venv`. In VS Code, run
**Python: Select Interpreter** from the Command Palette and choose the `.venv`.

**`Directory '.[gui]' is not installable. Neither 'setup.py' nor 'pyproject.toml' found.`**
You're running `pip` from the wrong folder. `cd` into the directory that contains
`pyproject.toml` (check with `ls pyproject.toml`), then re-run the install.

**The GUI won't open / `No module named '_tkinter'`**
Tkinter isn't bundled with your Python build. On macOS Homebrew Python, install
the package matching your Python version (e.g. `brew install python-tk@3.14`),
then try again. Command-line mode works without Tkinter.

---

## 🧪 Development

Set up an editable install with the dev tools (pytest + ruff):

```bash
pip install -e ".[dev]"
```

Run the test suite and linter:

```bash
pytest
ruff check .
```

Continuous integration (GitHub Actions) runs the same checks across Python 3.9,
3.11, and 3.12 on every push and pull request — see
[`.github/workflows/ci.yml`](.github/workflows/ci.yml).

---

## 🏷️ Versioning

This project follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`):

- **MAJOR** — incompatible or breaking changes
- **MINOR** — new features, backward compatible
- **PATCH** — bug fixes, backward compatible

The version is single-sourced from `__version__` in `src/ics_merger/__init__.py`
(read automatically by `pyproject.toml`). When releasing a new version, bump that
value, add a row to the changelog below, update the badge, and tag the release:

```bash
git tag -a v1.1.0 -m "v1.1.0"
git push origin v1.1.0
```

> 💡 Pushing a tag lets you publish a matching **GitHub Release**, which then
> appears automatically under the repository's **Releases** section.

### 📜 Changelog

| Version | Date       | Changes                                                                     |
| ------- | ---------- | --------------------------------------------------------------------------- |
| 1.1.0   | 2026-06-21 | Add drag-and-drop GUI; adopt a `src/` package layout with `pyproject.toml` packaging, an `ics-merger` console script, pytest tests, and GitHub Actions CI. |
| 1.0.0   | 2026-06-21 | Initial release: directory merge, dedup cache, and chunked output.          |

---

## 📄 License

Released under the [MIT License](LICENSE).
