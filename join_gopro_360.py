"""
Script to join GoPro 360 video files by group ID.

This script processes GoPro 360 video files with the naming pattern GSnnGGGG.360,
groups them by the last 4 digits (group ID), and concatenates files in each group
using ffmpeg and udtacopy.
"""
import os
import re
import subprocess
from pathlib import Path
import shutil

# Path to executables
udtacopy_path = Path("C:/bin/udtacopy.exe")
ffmpeg_path = Path("C:/ProgramData/chocolatey/bin/ffmpeg.exe")

# Ensure joined_files/ directory exists
joined_files_dir = Path("joined_files")
joined_files_dir.mkdir(exist_ok=True)

# Match GSnnGGGG.360 pattern
pattern = re.compile(r"GS\d{6}\.360")

# Group files by last 4 digits (group ID)
groups = {}
for filename in sorted(os.listdir()):
    if not pattern.match(filename):
        continue
    group_id = filename[4:8]  # characters 5–8
    groups.setdefault(group_id, []).append(filename)

# Process only groups with more than one file
for group_id, group_files in groups.items():
    if len(group_files) < 2:
        print(f"Skipping group {group_id} (only one file)")
        continue

    print(f"Processing group {group_id} with {len(group_files)} files...")

    group_files.sort()

    filelist_path = joined_files_dir / f"filelist_{group_id}.txt"
    with filelist_path.open("w", encoding="utf-8") as f:
        for filename in group_files:
            abs_path = Path(filename).resolve()
            f.write(f"file '{abs_path.as_posix()}'\n")

    temp_output = Path(f"temp_{group_id}.mp4")
    final_output = Path(f"{group_id}.360")

    subprocess.run([
        ffmpeg_path, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(filelist_path),
        "-c", "copy",
        "-ignore_unknown",
        "-map", "0:0", "-map", "0:1", "-map", "0:3", "-map", "0:5",
        str(temp_output)
    ], check=True)

    first_file = Path(group_files[0]).resolve()
    result = subprocess.run([
        str(udtacopy_path),
        str(first_file),
        str(temp_output)
    ], check=False)

    if result.returncode not in (0, 1):
        raise RuntimeError(f"udtacopy failed for group {group_id} with code {result.returncode}")

    temp_output.rename(final_output)

    # Set output timestamps to match first input file
    first_stat = os.stat(first_file)
    os.utime(final_output, (first_stat.st_atime, first_stat.st_mtime))

    # Move source files to joined_files/
    for filename in group_files:
        shutil.move(filename, joined_files_dir / filename)

    print(f"Finished: {final_output}")

print("All groups processed.")
