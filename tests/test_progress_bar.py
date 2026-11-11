"""Tests for songfetch.main.progress_bar edge cases."""

import songfetch.main as main


def test_progress_bar_zero_duration_nonzero_position(monkeypatch):
    """Unknown track length (duration 0) must not crash the bar."""
    monkeypatch.setattr(main, "get_position", lambda: 5000000)
    monkeypatch.setattr(main, "get_duration", lambda: 0)
    bar = main.progress_bar()
    assert "00:05 / 00:00" in bar
    assert "(0%)" in bar


def test_progress_bar_zero_duration_zero_position(monkeypatch):
    """Idle player (0/0) renders an empty bar instead of crashing."""
    monkeypatch.setattr(main, "get_position", lambda: 0)
    monkeypatch.setattr(main, "get_duration", lambda: 0)
    bar = main.progress_bar()
    assert "00:00 / 00:00" in bar
    assert "(0%)" in bar
