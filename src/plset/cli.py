import argparse
from pathlib import Path
import os

VALID_ACTIONS = {"union", "intersect", "diff", "xor"}
AUDIO_EXTENSIONS = {".mp3", ".flac", ".wav", ".ogg", ".m4a", ".aac"}


# --------------------------------------------------
# Input Handling
# --------------------------------------------------

def load_playlist(path: Path):
    tracks = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                tracks.append(line)
    return tracks


def scan_directory(path: Path):
    tracks = []
    for file in path.rglob("*"):
        if file.suffix.lower() in AUDIO_EXTENSIONS:
            tracks.append(str(file.resolve()))
    return sorted(tracks)


def load_input(path_str: str):
    path = Path(path_str)

    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")

    if path.is_dir():
        return scan_directory(path)
    else:
        return load_playlist(path)


# --------------------------------------------------
# Set Operations (Order Preserving)
# --------------------------------------------------

def union(a, b):
    seen = set()
    result = []
    for track in a + b:
        if track not in seen:
            seen.add(track)
            result.append(track)
    return result


def intersect(a, b):
    b_set = set(b)
    return [track for track in a if track in b_set]


def diff(a, b):
    b_set = set(b)
    return [track for track in a if track not in b_set]


def xor(a, b):
    a_set = set(a)
    b_set = set(b)
    return [track for track in a + b if (track in a_set) ^ (track in b_set)]


OPERATIONS = {
    "union": union,
    "intersect": intersect,
    "diff": diff,
    "xor": xor,
}


# --------------------------------------------------
# Output Handling
# --------------------------------------------------

def derive_output_name(a, action, b):
    name_a = Path(a).stem
    name_b = Path(b).stem
    return f"{name_a}_{action}_{name_b}.m3u8"


def make_relative(tracks, base: Path):
    relative_tracks = []
    for track in tracks:
        try:
            relative_tracks.append(str(Path(track).relative_to(base)))
        except ValueError:
            # If not relative to base, keep original
            relative_tracks.append(track)
    return relative_tracks


def write_playlist(path: Path, tracks, relative=False):
    if relative:
        base = path.parent.resolve()
        tracks = make_relative(tracks, base)

    with path.open("w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for track in tracks:
            f.write(track + "\n")


# --------------------------------------------------
# CLI
# --------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Playlist set algebra CLI tool"
    )

    parser.add_argument(
        "action",
        nargs="?",
        choices=VALID_ACTIONS,
        help="Set operation"
    )

    parser.add_argument("A", nargs="?")
    parser.add_argument("B", nargs="?")

    parser.add_argument(
        "--build",
        metavar="DIR",
        help="Build playlist from a single directory"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output playlist filename (.m3u8)"
    )

    parser.add_argument(
        "--relative",
        action="store_true",
        help="Write relative paths in output playlist"
    )

    args = parser.parse_args()

    # --- Build mode ---
    if args.build:
        tracks = scan_directory(Path(args.build))

        output_name = args.output or f"{Path(args.build).stem}.m3u8"
        output_path = Path(output_name).with_suffix(".m3u8")

        write_playlist(output_path, tracks, relative=args.relative)
        print(f"Created {output_path} ({len(tracks)} tracks)")
        return

    # --- Set operation mode ---
    if not (args.action and args.A and args.B):
        parser.error("Must provide action and two inputs, or use --build")

    tracks_a = load_input(args.A)
    tracks_b = load_input(args.B)

    result = OPERATIONS[args.action](tracks_a, tracks_b)

    output_name = args.output or derive_output_name(
        args.A, args.action, args.B
    )

    output_path = Path(output_name).with_suffix(".m3u8")

    write_playlist(output_path, result, relative=args.relative)

    print(f"Created {output_path} ({len(result)} tracks)")