# GoPro 360 Video Joiner

A Python script to automatically join GoPro 360 video files by group ID using ffmpeg and udtacopy.

## Overview

This script processes GoPro 360 video files with the naming pattern `GSnnGGGG.360`, groups them by the last 4 digits (group ID), and concatenates files in each group. It's designed to handle the split video files that GoPro cameras create for long recordings.

## Features

- Automatically detects and groups GoPro 360 files by group ID
- Concatenates video files using ffmpeg
- Preserves metadata using udtacopy
- Maintains original file timestamps
- Organizes processed files in a backup directory
- Skips groups with only one file

## Prerequisites

### Required Software

1. **Python 3.6+**
2. **ffmpeg** - Install via:
   - Windows: `choco install ffmpeg` (using Chocolatey)
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` (Ubuntu/Debian)
3. **udtacopy** - Tool for copying GoPro metadata
   - Download from the appropriate source and place in `C:/bin/` (Windows)

### File Structure

Before running the script, ensure your directory contains GoPro 360 files with the naming pattern:
```
GS011578.360
GS021578.360
GS011588.360
GS021588.360
...
```

## Installation

1. Clone this repository or download the script
2. Ensure the required software is installed
3. Update the executable paths in the script if needed:
   ```python
   udtacopy_path = Path("C:/bin/udtacopy.exe")  # Update this path
   ffmpeg_path = Path("C:/ProgramData/chocolatey/bin/ffmpeg.exe")  # Update this path
   ```

## Usage

1. Place the script in a directory containing your GoPro 360 files
2. Run the script:
   ```bash
   python join_gopro_360.py
   ```

## How It Works

1. **File Detection**: Scans the current directory for files matching the pattern `GSnnGGGG.360`
2. **Grouping**: Groups files by the last 4 digits (characters 5-8) of the filename
3. **Processing**: For each group with multiple files:
   - Creates a filelist for ffmpeg concatenation
   - Runs ffmpeg to join the video streams
   - Uses udtacopy to preserve GoPro metadata
   - Sets output timestamps to match the first input file
   - Moves source files to the `joined_files/` directory

## Output

- **Joined files**: `GGGG.360` (where GGGG is the group ID)
- **Backup directory**: `joined_files/` contains:
  - Original source files
  - Filelist files used by ffmpeg

## Example

Given these input files:
```
GS011578.360
GS021578.360
GS011588.360
GS021588.360
```

The script will create:
```
1578.360  (joined from GS011578.360 + GS021578.360)
1588.360  (joined from GS011588.360 + GS021588.360)
```

And move the original files to:
```
joined_files/
├── GS011578.360
├── GS021578.360
├── GS011588.360
├── GS021588.360
├── filelist_1578.txt
└── filelist_1588.txt
```

## Configuration

You can modify these variables at the top of the script:

```python
# Path to executables
udtacopy_path = Path("C:/bin/udtacopy.exe")
ffmpeg_path = Path("C:/ProgramData/chocolatey/bin/ffmpeg.exe")

# Output directory name
joined_files_dir = Path("joined_files")
```

## Troubleshooting

### Common Issues

1. **"udtacopy failed"**: Ensure udtacopy is installed and the path is correct
2. **"ffmpeg not found"**: Verify ffmpeg is installed and in PATH or update the path
3. **No files processed**: Check that your files match the `GSnnGGGG.360` pattern
4. **Permission errors**: Ensure the script has write permissions in the directory

### Error Codes

- **udtacopy return codes**: 0 and 1 are considered success
- **ffmpeg errors**: Will cause the script to stop with an error message

## License

This script is provided as-is for personal use. Modify as needed for your specific requirements.

## Contributing

Feel free to submit issues or pull requests to improve the script.
