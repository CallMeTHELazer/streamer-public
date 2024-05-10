Streamer: Stream Random Media from JSON Files (with ffmpeg Integration)

This project provides a Python script (streamer.py) designed to play random media files (series, movies, youtube videos) from specified JSON playlists, leveraging the powerful ffmpeg tool for media playback and streaming.

Features

    Plays media files from JSON playlists.
    Supports shuffling of playlists for random playback.
    Can handle override functionality to play a specific file.
    Integrates with ffmpeg for media playback (separate installation required).
    Offers multiple bitrate options for streaming (configuration needed).

Installation

    Ensure you have Python 3 installed.
    Install required libraries (may vary based on your setup):
    Bash

    pip install argparse

    Use code with caution.

    Install ffmpeg and ffprobe utilities. Refer to their official documentation for specific installation instructions.

Usage

    Place your JSON media playlists in the appropriate locations (e.g., /home/user/streamer-public/json_directory.json).
    Run the script with desired arguments:
        -s or --series_file: Play Series.
        -m or --movies_file: Play Movies.
        -y or --youtube: Play Youtube.
        -o or --override: Path to a specific file to play (overrides playlist selection).
        --shuffle: Enables shuffling of playlists before playback.
        --dry: Enables dry run mode (simulates playback without playing media).

Example Usage
Bash

python streamer.py -s /path/to/series.json -m /path/to/movies.json --shuffle --bitrate=512k

Use code with caution.

This command will play random media files from the provided series and movies JSON files, shuffling the playlists first and using a bitrate of 512kbps for streaming (assuming the script is configured for bitrate selection).

Configuration

The script utilizes a separate function (player.py) for ffmpeg integration. This function offers placeholders for bitrate options within the ffmpeg command. You'll need to replace these placeholders with your desired bitrate values (e.g., "256k", "1024k") in the player.py file.

Notes

    The jsoner module is assumed to be a custom module for loading and saving JSON data. You'll need to implement this module or use an existing JSON library like json.
    Refer to the ffmpeg documentation for detailed information on available options and functionalities.
    Error handling within the script might require further customization based on your specific needs.

Contributing

If you'd like to contribute to this project, feel free to reach out to the repository owner for specific guidelines.

License

The license for this project is currently unspecified. Please refer to the repository or contact the owner for clarification.