import os
import re
from songfetch.ascii_convert import convert
from songfetch.player_utils import (
    get_art,
    get_loop,
    get_shuffle,
    get_player_name,
    get_status,
    get_title,
    get_artist,
    get_album,
    get_duration_formatted,
    get_user,
    get_volume,
    get_url,
    get_backend,
    get_duration,
    get_position
)

# Regex to detect and remove ANSI color codes for spacing fix
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

def strip_ansi(s: str) -> str:
    # Remove color escape sequences
    return ANSI_RE.sub("", s)

def ljust_ansi(s: str, width: int) -> str:
    # Pad based on visible width, ignoring escape codes
    pad = width - len(strip_ansi(s))
    if pad > 0:
        return s + " " * pad
    return s

def progress_bar():
    # Calculate progress bar state
    pos = get_position()
    dur = get_duration()
    if pos == 0 or dur == 0:
        percentage = 0
    else:
        percentage = pos / dur

    # Fill ratio
    filled = int(percentage * 16)
    empty = 16 - filled
    fprint = "▓" * filled
    eprint = "░" * empty

    # Convert to seconds
    pos_seconds = int(pos / 1000000)
    dur_seconds = int(dur / 1000000)

    # Display formatted time
    display_pos = f"{pos_seconds // 60:02d}:{pos_seconds % 60:02d}"
    display_dur = f"{dur_seconds // 60:02d}:{dur_seconds % 60:02d}"

    # Combine
    display_str = f"\033[0m {display_pos} / {display_dur} ({round(percentage * 100)}%)"
    return fprint + eprint + display_str

def get_info_line():
    # Text labels
    line = f"\033[34m─────────────────────────────────────────\033[0m"
    now_playing = "Now Playing"
    playback_info = "Playback Info"
    audio_system = "Audio System"

    # Color palette preview
    normal = ""
    bright = ""
    for i in range(8):
        normal += f"\033[4{i}m   \033[0m"
    for i in range(8):
        bright += f"\033[10{i}m   \033[0m"

    # Assemble right‑side info panel
    info_lines = [
        f"\033[1;34m{get_user()}\033[0m@\033[1;34m{get_player_name()}\033[0m",
        line,
        f"\033[97m{now_playing}\033[0m",
        line,
        f"\033[34mTitle\033[0m: {get_title()}",
        f"\033[34mArtist\033[0m: {get_artist()}",
        f"\033[34mAlbum\033[0m: {get_album()}",
        f"\033[34mDuration\033[0m: {get_duration_formatted()}",
        f"\033[34m{progress_bar()}\033[0m",
        line,
        f"\033[97m{playback_info}\033[0m",
        line,
        f"\033[34mStatus\033[0m: {get_status()}",
        f"\033[34mVolume\033[0m: {get_volume()}",
        f"\033[34mLoop\033[0m: {get_loop()}",
        f"\033[34mShuffle\033[0m: {get_shuffle()}",
        f"\033[34mPlayer\033[0m: {get_player_name()}",
        f"\033[34mURL\033[0m: {get_url()}",
        line,
        f"\033[97m{audio_system}\033[0m",
        line,
        f"\033[34mBackend\033[0m: {get_backend()}",
        "",
        normal,
        bright
    ]
    return info_lines

def main():
    # Get terminal width
    columns = os.get_terminal_size().columns
    max_width = 104

    if columns < max_width:
        # Too small to display artwork properly
        art_col = []
        max_art = 2
    else:
        # Generate ASCII art
        art_col = convert(get_art())
        # Calculate visible width (ignores color codes)
        max_art = max(len(strip_ansi(x)) for x in art_col)

    # Always get right column info
    info_col = get_info_line()
    max_info = max(len(strip_ansi(y)) for y in info_col[:-2])

    # Align both columns side by side
    if len(art_col) > len(info_col):
        new_info_col = info_col + [''] * (len(art_col) - len(info_col))
        for i in range(len(art_col)):
            print(f"{ljust_ansi(art_col[i], max_art + 1)}{new_info_col[i]}")
    else:
        new_art_col = art_col + [''] * (len(info_col) - len(art_col))
        for j in range(len(info_col)):
            print(f"{ljust_ansi(new_art_col[j], max_art + 1)}{info_col[j]}")

# Run program
if __name__ == "__main__":
    main()
