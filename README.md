# plset

A small CLI tool for performing **set algebra on playlists**.

`plset` lets you treat playlists (or directories of audio files) as sets and perform operations like:

- union
- intersection
- difference
- symmetric difference (xor)

It outputs a valid `.m3u8` playlist file.

## Features

- Supports `.m3u` and `.m3u8` playlists
- Supports directories (recursively scans for audio files)
- Order-preserving set operations
- Optional relative path output
- Can build a playlist directly from a directory
- No external dependencies
- Windows-friendly

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/plset.git
cd plset
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
.venv\Scripts\Activate
```

From the project root:

```bash
pip install .
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/Heros-Tempus/plset.git
```

- You can verify the installation by running:

```bash
plset --help
```

## Usage

### Set Operations

```bash
plset [union|intersect|diff|xor] A B
```

Where `A` and `B` can be:

- A playlist file (`.m3u` or `.m3u8`)
- A directory (recursively scanned for audio files)

Example:

```bash
plset diff A.m3u8 B.m3u8
```

By default this creates:

```bash
A_diff_B.m3u8
```

You can specify an output file:

```bash
plset union chill.m3u8 upbeat.m3u8 -o combined.m3u8
```

### Build Playlist from a Directory

```bash
plset --build MusicFolder
```

Creates:

```bash
MusicFolder.m3u8
```

With custom name:

```bash
plset --build MusicFolder -o library.m3u8
```

### Relative Paths

To write relative paths in the output playlist:

```bash
plset diff A B --relative
```

Relative paths are calculated from the output file’s directory.

## Supported Audio Extensions

- `.mp3`
- `.flac`
- `.wav`
- `.ogg`
- `.m4a`
- `.aac`

## Set Operation Behavior

| Action | Description |
| ------------- | ------------- |
| union | All tracks from A and B, no duplicates |
| intersect | Tracks present in both A and B |
| diff | Tracks in A but not in B |
| xor | Tracks in A or B but not both |

All operations preserve the order of playlist A where applicable.

## Examples

Subtract sleep tracks from a full library:

```bash
plset diff full_library.m3u8 sleep_tracks.m3u8
```

Combine two folders:

```bash
plset union JazzFolder RockFolder
```

Find common tracks between two playlists:

```bash
plset intersect playlist1.m3u8 playlist2.m3u8
```

## Development

Run tests:

```bash
pytest
```

Project structure:

```bash
plset/
├── pyproject.toml
├── src/plset/
│   ├── __init__.py
│   └── cli.py
└── tests/
```

## Design Notes

- Paths from existing playlists are preserved exactly.
- Directory scans use absolute paths.
- No destructive normalization is performed.
- Relative path conversion happens only at write time.

The goal is predictable behavior that works reliably with VLC and other media players.
