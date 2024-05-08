import subprocess
from random import shuffle
import tools.jsoner as jsoner
import time
import argparse

parser = argparse.ArgumentParser(description="Runs a bump poined at the webserver")
parser.add_argument("-s", "--software", action="store_true", dest="software",
                    help="Run stream in software mode (Default False)", required=False)
parser.add_argument("-b", "--bump_file", action="store", dest="bump_file",
                    type=str, help="Input the bump json file path", required=True)
args = parser.parse_args()

# bump_files = "/home/pokeruadmin/streamer/json_bumps.json"
bump_files = args.bump_file

def player(files_list):
        # files_list = jsoner.loader(json_file,"filenames")

        for i, filename in enumerate(files_list):
            print("In For Loop")
            
            if args.software is not True:
                ffmpeg_command = [
                                    "ffmpeg",  # Path to the ffmpeg executable
                                    "-y",        # Overwrite output files
                                    "-hwaccel",  # Enable hardware acceleration
                                    "cuda",      # Use CUDA for hardware acceleration
                                    "-hwaccel_output_format", "cuda",  # Use CUDA for output format
                                    "-re",        # Repeat input (useful for streams)
                                    "-i", filename,  # Input file path (replace with actual filename variable)
                                    "-c:a", "aac",  # Audio codec: aac
                                    "-ac", "2",     # Audio channels: 2
                                    "-ar", "22050",  # Audio sample rate: 22050 Hz
                                    "-c:v", "h264_nvenc",  # Video codec: h264 using NVENC encoder
                                    "-maxrate", "25000k",  # Maximum bitrate: 25000 kbps
                                    "-bufsize", "1000k",    # Buffer size: 1000 kb
                                    "-b:v", "5M",      # Video bitrate: 5 Mbps
                                    "-map", "0:s:m:language:eng?",  # Map subtitle stream with language code "eng" (English)
                                    "-f", "flv",     # Output format: FLV
                                    "rtmp://10.0.0.19/live/stream"  # Destination URL for streaming
                                ]
            else:
                ffmpeg_command = [
                                    "ffmpeg",  # Path to the ffmpeg executable
                                    "-y",        # Overwrite output files
                                    "-re",        # Repeat input (useful for streams)
                                    "-i", filename,  # Input file path (replace with actual filename variable)
                                    "-c:a", "aac",  # Audio codec: aac
                                    "-ac", "2",     # Audio channels: 2
                                    "-ar", "22050",  # Audio sample rate: 22050 Hz
                                    "-c:v", "libx264",  # Video codec: h264 using Lib encoder
                                    "-maxrate", "25000k",  # Maximum bitrate: 25000 kbps
                                    "-bufsize", "1000k",    # Buffer size: 1000 kb
                                    "-b:v", "5M",      # Video bitrate: 5 Mbps
                                    "-f", "flv",     # Output format: FLV
                                    "rtmp://10.0.0.19/live/stream"  # Destination URL for streaming
                                ]
            print(ffmpeg_command)

            # ffmpeg_command = f"ffmpeg -y -hwaccel cuda -hwaccel_output_format cuda -re -i \"{filename}\" -c:a aac -ac 2 -ar 22050 -c:v h264_nvenc  -maxrate 25000k -bufsize 1000k -b:v 5M  -f flv rtmp://10.0.0.19/live/stream"
            result = subprocess.run(ffmpeg_command, capture_output=True)
            output = result.stderr.decode("utf-8")
            print(output)
            if "Server error: Already publishing" not in output:
                time.sleep(6)
                break
            else:
                print("Error: Stream already publishing. Retrying in 5 seconds.")
                time.sleep(4)
                break

if __name__ == "__main__":
    while True:
        files = jsoner.loader(bump_files,"filenames")

        shuffle(files)

        player(files)