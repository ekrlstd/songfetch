import os
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

def progress_bar():
    # Calculate percentage
    pos = get_position()
    dur = get_duration()
    if pos == 0 or dur == 0:
        percentage = 0
    else:
        percentage = pos / dur

    # Calculate filled and empty characters
    filled = int(percentage * 16)
    empty = 16 - filled
    fprint = "▓" * filled
    eprint = "░" * empty

    # Calculate position and duration seperately
    pos_seconds = int(pos / 1000000)
    dur_seconds = int(dur / 1000000)

    # Nicer representation
    display_pos = f"{pos_seconds // 60:02d}:{pos_seconds % 60:02d}"
    display_dur = f"{dur_seconds // 60:02d}:{dur_seconds % 60:02d}"

    # Full representation
    display_str = f"\033[0m {display_pos} / {display_dur} ({round(percentage * 100)}%)"

    return fprint + eprint + display_str

def get_info_line():
    # Get some strings to use later
    line = f"\033[34m─────────────────────────────────────────\033[0m"
    now_playing = "Now Playing"
    playback_info = "Playback Info"
    audio_system = "Audio System"

    normal = ""
    bright = ""

    # Ansi palette
    for i in range(8):  # Normal colors (0-7)
        normal += f"\033[4{i}m   \033[0m"
    for i in range(8):  # Bright colors (0-7 in bright)
        bright += f"\033[10{i}m   \033[0m"

    # Here we concatenate all the info into one list
    # Use ANSI escape sequences to style the colors
    info_lines = [
    # Print username and track data
    f"\033[1;34m{get_user()}\033[0m@\033[1;34m{get_player_name()}\033[0m",
    line, f"\033[97m{now_playing}\033[0m", line,
    f"\033[34mTitle\033[0m: {get_title()}",
    f"\033[34mArtist\033[0m: {get_artist()}",
    f"\033[34mAlbum\033[0m: {get_album()}",
    f"\033[34mDuration\033[0m: {get_duration_formatted()}",
    f"\033[34m{progress_bar()}\033[0m",

    # Print player data
    line, f"\033[97m{playback_info}\033[0m", line,
    f"\033[34mStatus\033[0m: {get_status()}",
    f"\033[34mVolume\033[0m: {get_volume()}",
    f"\033[34mLoop\033[0m: {get_loop()}",
    f"\033[34mShuffle\033[0m: {get_shuffle()}",
    f"\033[34mPlayer\033[0m: {get_player_name()}",
    f"\033[34mURL\033[0m: {get_url()}",

    # Print system data
    line, f"\033[97m{audio_system}\033[0m", line,
    f"\033[34mBackend\033[0m: {get_backend()}",
    "",
    # Print palette
    normal, bright
]
    return info_lines

# Main function
def main():
    # Get terminal size
    columns = os.get_terminal_size().columns
    max_width = 104  # Calculated max width

    if columns < max_width:
        # Set "empty" variables
        art_col = []
        max_art = 2

    # Only run if terminal's big enough
    else:
        art_col = convert(get_art())
        # Find the longest line in both column lists
        max_art = max(len(x) for x in art_col)

    # Always get info lines though
    info_col = get_info_line()
    max_info = max(len(y) for y in info_col[:-2])

    # Print lists next to each other when one list may be longer than the other:
    if len(art_col) > len(info_col):  # Compare lenghts
        # Replace but with added padding (spaces)
        new_info_col = info_col + [''] * (len(art_col) - len(info_col))
        # Loop through all lines in art
        for i in range(len(art_col)):
            print(f"{art_col[i]:{max_art-2}}{new_info_col[i]:{max_info}}")
    else:
        # Pad but the othre way around
        new_art_col = art_col + [''] * (len(info_col) - len(art_col))
        # Loop all lines in info
        for j in range(len(info_col)):
            print(f"{new_art_col[j]:{max_art-2}}{info_col[j]:{max_info}}")

# Run the program
if __name__ == "__main__":
    main()

# TODO: Add terminal colors at the end like fastfetch or onefetch
