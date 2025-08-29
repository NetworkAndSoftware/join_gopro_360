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

    # Create directory for this group
    group_dir = Path(group_id)
    group_dir.mkdir(exist_ok=True)

    # Move all files for this group into the directory
    for filename in group_files:
        source_path = Path(filename)
        dest_path = group_dir / filename
        shutil.move(str(source_path), str(dest_path))

    print(f"Finished: Created directory {group_id}/ with {len(group_files)} file(s)")

print("All groups processed.")
