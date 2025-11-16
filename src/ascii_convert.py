import urllib.parse, urllib.request, tempfile, io
from importlib import resources
from PIL import Image

def default_art(file="../assets/default_art.txt"):
    # Get the default music note art from file
    with resources.files("songfetch.assets").joinpath("default_art.txt").open("r", encoding="utf-8") as f:
        return f.read().split("\n")

# Art to ASCII
def convert(art_uri):
    # Init variables
    ascii_art_lines = None
    # Check file type
    if art_uri is None or art_uri.strip() == "":  # If return empty string
        return default_art()

    # File URI (local files)
    elif art_uri.startswith("file://"):
        try:
            # Strip "file://" prefix and decode
            new_uri = urllib.parse.unquote(art_uri[7:])
            img = Image.open(new_uri).convert("RGB")
        except Exception:
            return default_art()

    # Remote image URLs
    elif art_uri.startswith(("https://", "http://")):
        try:
            # Create a temporary file to store image in
            temp = tempfile.NamedTemporaryFile(delete=False)
            temp.close()
            # Get the image from the URL
            urllib.request.urlretrieve(art_uri, temp.name)
            img = Image.open(temp.name).convert("RGB")
        except Exception:
            return default_art()

    # Edge cases
    else:
        return default_art()

    # Convert image to true-color ASCII
    try:
        cols = 60
        width_ratio = 2.2  # Keep same proportions as original output
        w, h = img.size
        new_height = max(1, int((h / w) * cols / width_ratio))
        img = img.resize((cols, new_height))

        # Character ramp used to represent brightness
        chars = " .:-=+*#%@"
        ascii_art_lines = []

        for y in range(img.height):
            line = []
            for x in range(img.width):
                r, g, b = img.getpixel((x, y))
                brightness = (r + g + b) / 3
                # Always draw something (no empty gaps)
                idx = int(brightness / 255 * (len(chars) - 1))
                c = chars[idx]
                # Add true color ANSI values for each char
                line.append(f"\x1b[38;2;{r};{g};{b}m{c}\x1b[0m")
            # Small left indent, plus one trailing space for clean text separation
            ascii_art_lines.append("  " + "".join(line) + " ")

        # Add an empty line after art for spacing
        ascii_art_lines.append("")
        return ascii_art_lines

    except Exception:
        return default_art()
