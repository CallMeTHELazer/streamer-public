import subprocess  # Importing the subprocess module for running shell commands
import logging
import config_logging

#Logging Configurarion
logger = logging.getLogger(__name__)
log_level = getattr(logging, config_logging.logging_level.upper())
logging.basicConfig(level=log_level)
# logger.setLevel(logging.config_logging.logging_level)
file_handler = logging.FileHandler(config_logging.logging_file)
logger.addHandler(file_handler)

def player(filename, dry=False):
    # Define the ffprobe command to gather information about the media file
    logger.info(filename)
    ffprobe_command = [
        "ffprobe",  # Command name
        filename  # Input filename
    ]

    # If dry run is not enabled
    if not dry:
        # Run the ffprobe command and capture the output
        probe_result = subprocess.run(ffprobe_command, capture_output=True)
        # Decode the output to UTF-8 format
        ffprobe_result = probe_result.stderr.decode("utf-8")

        # Check for the audio stream in the ffprobe result
        for i in range(1, 10):
            audio_stream = str(i)
            # If English audio stream is found
            if f"Stream #0:{audio_stream}(eng): Audio:" in ffprobe_result:
                logger.info(f"Notice: English Audio Stream Found in stream 0:{audio_stream}")
                break
        else:
            # If English audio stream is not found, use the default audio stream (0:1)
            logger.error(f"Error: Could Not find English Audio Track, Defaulting to track 0:1. Please check the file with ffprobe {filename}")
            audio_stream = str(1)

        # Check for the subtitle stream in the ffprobe result
        for i in range(2, 20):
            subtitle_stream = str(i)
            # If English subtitle stream is found
            if f"Stream #0:{subtitle_stream}(eng)" in ffprobe_result:
                logger.info(f"Notice: English Subtitle Stream Found in stream 0:{subtitle_stream}")
                break
        else:
            # If English subtitle stream is not found
            logger.warning(f"Notice: Could Not find English Subtitle Track. If this is incorrect, Please check the file with ffprobe {filename}")

        # Define the ffmpeg command to play the media file
        ffmpeg_command = [
            "ffmpeg",  # Path to the ffmpeg executable
            "-y",  # Overwrite output files
            "-hwaccel", "cuda",  # Enable hardware acceleration
            "-hwaccel_output_format", "cuda",  # Use CUDA for output format
            "-re",  # Repeat input (useful for streams)
            "-i", filename,  # Input file path
            # Low Quality Stream
            "-c:v", "h264_nvenc", "-map", "0:0", "-map", f"0:{audio_stream}", "-map", f"0:{subtitle_stream}?",
            "-c:a", "aac", "-ac", "2", "-ar", "22050", "-b:v", "256k",
            "-hls_list_size", "0", "-f", "flv", "rtmp://10.0.0.19/hls/stream_low",
            # Mid Quality Stream
            "-c:v", "h264_nvenc", "-map", "0:0", "-map", f"0:{audio_stream}", "-map", f"0:{subtitle_stream}?",
            "-c:a", "aac", "-ac", "2", "-ar", "22050", "-b:v", "768k",
            "-hls_list_size", "0", "-f", "flv", "rtmp://10.0.0.19/hls/stream_mid",
            # High Quality Stream
            "-c:v", "h264_nvenc", "-map", "0:0", "-map", f"0:{audio_stream}", "-map", f"0:{subtitle_stream}?",
            "-c:a", "aac", "-ac", "2", "-ar", "22050", "-b:v", "1024k",
            "-hls_list_size", "0", "-f", "flv", "rtmp://10.0.0.19/hls/stream_high",
            # Higher Quality Stream
            "-c:v", "h264_nvenc", "-map", "0:0", "-map", f"0:{audio_stream}", "-map", f"0:{subtitle_stream}?",
            "-c:a", "aac", "-ac", "2", "-ar", "22050", "-b:v", "1920k",
            "-hls_list_size", "0", "-f", "flv", "rtmp://10.0.0.19/hls/stream_higher",
            # Source Quality Stream
            "-c:v", "h264_nvenc", "-map", "0:0", "-map", f"0:{audio_stream}", "-map", f"0:{subtitle_stream}?",
            "-c:a", "aac", "-ac", "2", "-ar", "22050", "-b:v", "10M",
            "-hls_list_size", "0", "-f", "flv", "rtmp://10.0.0.19/hls/stream_src"
        ]

        # Print the ffmpeg command for debugging
        logger.info(ffmpeg_command)
        # Print the message indicating the media file and audio stream being played
        logger.info(f"Notice: Playing \"{filename}\" with Audio stream \"{audio_stream}\".")
        # Run the ffmpeg command and capture the output
        ffmpeg_result = subprocess.run(ffmpeg_command, capture_output=True)
        # Decode the output to UTF-8 format
        ffmpeg_output = ffmpeg_result.stderr.decode("utf-8")
        # Print the ffmpeg output for debugging
        logger.info(ffmpeg_output)

        # If "Server error: Already publishing" not found in the ffmpeg output
        if "Server error: Already publishing" not in ffmpeg_output:
            return True  # Return True indicating successful playback
        else:
            logger.error("Error: Stream already publishing. Retrying in 5 seconds.")
            return False  # Return False indicating playback failure
    else:
        return True  # If dry run is enabled, return True without playing the media
