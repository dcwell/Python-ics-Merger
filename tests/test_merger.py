"""Unit tests for the ICS merge engine."""

import os
import textwrap

from ics_merger.merger import get_ics_files, merge_ics_files


def _write_ics(path, uid, summary):
    """Write a minimal single-event .ics file to ``path``."""
    path.write_text(textwrap.dedent(f"""\
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:-//test//
        BEGIN:VEVENT
        UID:{uid}
        DTSTART:20260101T100000Z
        DTEND:20260101T110000Z
        SUMMARY:{summary}
        END:VEVENT
        END:VCALENDAR
        """))


def test_merge_dedups_within_and_across_runs(tmp_path):
    a = tmp_path / "a.ics"
    b = tmp_path / "b.ics"
    c = tmp_path / "c.ics"
    _write_ics(a, "e1@test", "One")
    _write_ics(b, "e2@test", "Two")
    _write_ics(c, "e1@test", "One")  # duplicate of a

    out = tmp_path / "out"
    out.mkdir()

    added = merge_ics_files([str(a), str(b), str(c)], str(out))

    assert added == 2  # e1 and e2; the duplicate e1 is skipped
    assert (out / "merged_events_1.ics").exists()
    assert (out / "seen_events.json").exists()

    # Re-running must add nothing new because the cache persists.
    assert merge_ics_files([str(a), str(b), str(c)], str(out)) == 0


def test_get_ics_files_is_case_insensitive_and_filters(tmp_path):
    (tmp_path / "x.ics").write_text("")
    (tmp_path / "y.ICS").write_text("")
    (tmp_path / "z.txt").write_text("")

    found = sorted(os.path.basename(p) for p in get_ics_files(str(tmp_path)))

    assert found == ["x.ics", "y.ICS"]
