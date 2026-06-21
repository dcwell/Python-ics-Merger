"""Drag-and-drop GUI for the ICS Event Merger.

Provides a small Tkinter window where the user can drag and drop ``.ics`` files
(or folders containing them) and merge everything with one click. True
drag-and-drop relies on the optional :mod:`tkinterdnd2` package; when it is not
installed, :func:`run_gui` transparently falls back to a native multi-select
file picker so the tool still works without extra dependencies.

All Tkinter imports are performed lazily inside the functions so that importing
this module never fails on headless systems that lack a display or Tk.
"""

import os

from .merger import get_ics_files, merge_ics_files


def run_gui():
    """Launch the drag-and-drop window for merging .ics files.

    Falls back to :func:`_run_picker_gui` when ``tkinterdnd2`` is unavailable.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except ImportError:
        print(
            "Tkinter isn't available for this Python install, so the GUI can't "
            "start.\n"
            "  - On macOS (Homebrew): brew install python-tk\n"
            "  - Or merge from the command line: "
            "python ICS_Merger.py <directory_path>"
        )
        return

    try:
        from tkinterdnd2 import DND_FILES, TkinterDnD
    except ImportError:
        _run_picker_gui()
        return

    selected = {}  # path -> None: keeps entries unique while preserving order

    def add_paths(paths):
        for p in paths:
            p = p.strip()
            if not p:
                continue
            if os.path.isdir(p):
                for f in get_ics_files(p):
                    selected[os.path.abspath(f)] = None
            elif p.lower().endswith(".ics"):
                selected[os.path.abspath(p)] = None
        refresh()

    def refresh():
        listbox.delete(0, tk.END)
        for p in selected:
            listbox.insert(tk.END, os.path.basename(p))
        count_var.set(f"{len(selected)} file(s) ready")

    def on_drop(event):
        add_paths(root.tk.splitlist(event.data))

    def browse():
        add_paths(filedialog.askopenfilenames(
            title="Select .ics files",
            filetypes=[("iCalendar files", "*.ics")],
        ))

    def clear():
        selected.clear()
        refresh()

    def do_merge():
        if not selected:
            messagebox.showwarning("No files", "Add some .ics files first.")
            return
        output_dir = filedialog.askdirectory(title="Choose an output folder")
        if not output_dir:
            return
        total = merge_ics_files(list(selected), output_dir)
        messagebox.showinfo(
            "Merge complete",
            f"Added {total} new events.\n\nSaved to:\n{output_dir}",
        )

    root = TkinterDnD.Tk()
    root.title("ICS Event Merger")
    root.geometry("520x440")
    root.minsize(420, 360)

    drop = tk.Label(
        root,
        text="\U0001F4E5  Drag & drop .ics files (or folders) here",
        relief="ridge", bd=2, height=4, bg="#f0f0f0",
    )
    drop.pack(fill="x", padx=12, pady=12)
    drop.drop_target_register(DND_FILES)
    drop.dnd_bind("<<Drop>>", on_drop)

    listbox = tk.Listbox(root)
    listbox.pack(fill="both", expand=True, padx=12)

    count_var = tk.StringVar(value="0 file(s) ready")
    tk.Label(root, textvariable=count_var).pack(pady=4)

    btns = tk.Frame(root)
    btns.pack(pady=8)
    tk.Button(btns, text="Add files\u2026", command=browse).pack(side="left", padx=4)
    tk.Button(btns, text="Clear", command=clear).pack(side="left", padx=4)
    tk.Button(btns, text="Merge \u25B6", command=do_merge).pack(side="left", padx=4)

    root.mainloop()


def _run_picker_gui():
    """Fallback GUI used when ``tkinterdnd2`` is not installed.

    Presents native file/folder pickers instead of a drag-and-drop window.
    """
    import tkinter as tk
    from tkinter import filedialog, messagebox

    tk.Tk().withdraw()
    messagebox.showinfo(
        "ICS Event Merger",
        "Drag-and-drop needs the tkinterdnd2 package "
        "(pip install tkinterdnd2).\n\n"
        "Select your .ics files instead.",
    )
    files = filedialog.askopenfilenames(
        title="Select .ics files",
        filetypes=[("iCalendar files", "*.ics")],
    )
    if not files:
        return
    output_dir = filedialog.askdirectory(title="Choose an output folder")
    if not output_dir:
        return
    total = merge_ics_files(list(files), output_dir)
    messagebox.showinfo(
        "Merge complete",
        f"Added {total} new events.\n\nSaved to:\n{output_dir}",
    )
