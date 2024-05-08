Streamer Script - Random Media Player

This Python script plays random media files (series or movies) from specified JSON files and streams them using ffmpeg.

Requirements:

    Python 3
    ffmpeg and ffprobe installed
    jsoner.py module (assumed to be a custom module for handling JSON files)
    ffmpeg_player.py module (assumed to be a custom module for ffmpeg interactions)

Usage:

python streamer.py [options]

Options:

    -s, --series_file: Path to the JSON file containing a list of series filenames.
    -m, --movies_file: Path to the JSON file containing a list of movie filenames.
    -o, --override_file: Path to a specific media file to play (overrides series/movies).
    --shuffle: Enable shuffling of files within each category (series/movies).
    --dry: Dry run mode - performs ffprobe analysis but doesn't stream using ffmpeg.

Example:

python streamer.py -s /path/to/series.json -m /path/to/movies.json --shuffle

This command plays a random series or movie from the specified JSON files, shuffling the lists beforehand.

How it Works:

    The script parses command-line arguments using argparse.
    Based on arguments, it determines the media type (series/movies) and whether to shuffle the lists.
    It uses jsoner.loader to load filenames from the specified JSON files.
    If --shuffle is enabled, it shuffles the filenames using shuffle_files.
    The play_random_media function chooses a media type (randomly if both series/movies are provided) and iterates through the shuffled list.
    For each file, it uses ffmpeg_player.player to perform the following:
        Analyzes the file with ffprobe to identify audio and subtitle streams (focusing on English tracks).
        Constructs an ffmpeg command for streaming with appropriate audio/video codecs, bitrates, and output format (FLV in this case).
        Executes the ffmpeg command and handles potential errors like "Server error: Already publishing".

Notes:

    The script relies on the jsoner.py and ffmpeg_player.py modules, which are not included here.
    You might need to adjust ffmpeg options like bitrates and output format based on your streaming requirements.
    Error handling can be further improved for robust operation.