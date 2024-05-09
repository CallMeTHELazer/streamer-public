import subprocess

def player(filename,dry=False):

        ffprobe_command = [
                            "ffprobe",
                            filename
                        ]

        if dry is not True:

            probe_result = subprocess.run(ffprobe_command, capture_output=True)
            ffprobe_result = probe_result.stderr.decode("utf-8")
            # print("***OUTPUT OF FFPROBE***")
            # print(ffprobe_result)
            # print("***END OF FFPROBE OUTPUT")

            for i in range(1,10):
                audio_stream = str(i)
                if f"Stream #0:{audio_stream}(eng): Audio:" in ffprobe_result:
                    print(f"Notice: English Audio Stream Found in stream 0:{audio_stream}")
                    break
            else:
                print(f"Error: Could Not find English Audio Track, Defaulting to track 0:1. Please check the file with ffprobe {filename}")
                audio_stream = str(1)
            for i in range(2,20):
                subtitle_stream = str(i)
                if f"Stream #0:{subtitle_stream}(eng)" in ffprobe_result:
                    print(f"Notice: English Subtitle Stream Found in stream 0:{subtitle_stream}")
                    break
            else:
                print(f"Notice: Could Not find English Subtitle Track. If this is incorrect, Please check the file with ffprobe {filename}")
                subtitle_stream = str(2)


            ffmpeg_command = [
                                "ffmpeg",  # Path to the ffmpeg executable
                                "-y",       # Overwrite output files
                                "-hwaccel",  # Enable hardware acceleration
                                "cuda",      # Use CUDA for hardware acceleration
                                "-hwaccel_output_format", "cuda",  # Use CUDA for output format
                                "-re",        # Repeat input (useful for streams)
                                "-i", filename,  # Input file path (replace with actual filename variable)
                                # "-c:v", "h264_nvenc",  # Video codec: h264 using NVENC encoder
                                # "-map", "0:v",
                                # "-map", f"0:{audio_stream}",  # Selects the the English audio
                                # "-map", f"0:{subtitle_stream}?",
                                # "-c:a", "aac",  # Audio codec: aac
                                # "-ac", "2",     # Audio channels: 2
                                # "-ar", "22050",  # Audio sample rate: 22050 Hz
                                # "-maxrate", "10M",  # Maximum bitrate: 25000 kbps
                                "-bufsize", "1000k",    # Buffer size: 1000 kb
                                # "-b:v", "5M",      # Video bitrate: 5 Mbps
                                # "-f", "flv",     # Output format: FLV
                                # "rtmp://10.0.0.19/live/stream"  # Destination URL for streaming
                                
                                #Low Quality Stream
                                
                                "-c:v", "h264_nvenc",  # Video codec: h264 using NVENC encoder
                                "-map", "0:0",
                                "-map", f"0:{audio_stream}",  # Selects the the English audio
                                "-map", f"0:{subtitle_stream}?",
                                "-c:a", "aac",  # Audio codec: aac
                                "-ac", "2",     # Audio channels: 2
                                "-ar", "22050",  # Audio sample rate: 22050 Hz
                                "-b:v", "256k",      # Video bitrate: 5 Mbps
                                # "-vf", "'scale=480:trunc(ow/a/2)*2'", #Will Figure out how this works later
                                "-hls_list_size", "0",
                                "-f", "flv",
                                "rtmp://10.0.0.19/hls/stream_low",  # Destination URL for streaming

                                #Mid Quality Stream
                                
                                "-c:v", "h264_nvenc",  # Video codec: h264 using NVENC encoder
                                "-map", "0:0",
                                "-map", f"0:{audio_stream}",  # Selects the the English audio
                                "-map", f"0:{subtitle_stream}?",
                                "-c:a", "aac",  # Audio codec: aac
                                "-ac", "2",     # Audio channels: 2
                                "-ar", "22050",  # Audio sample rate: 22050 Hz
                                "-b:v", "768k",      # Video bitrate: 256k
                                # "-vf", "scale=480:trunc(ow/a/2)*2", #Will Figure out how this works later
                                "-hls_list_size", "0",
                                "-f", "flv",
                                "rtmp://10.0.0.19/hls/stream_mid",  # Destination URL for streaming

                                #High Quality Stream
                                
                                "-c:v", "h264_nvenc",  # Video codec: h264 using NVENC encoder
                                "-map", "0:0",
                                "-map", f"0:{audio_stream}",  # Selects the the English audio
                                "-map", f"0:{subtitle_stream}?",
                                "-c:a", "aac",  # Audio codec: aac
                                "-ac", "2",     # Audio channels: 2
                                "-ar", "22050",  # Audio sample rate: 22050 Hz
                                "-b:v", "1024k",      # Video bitrate: 5 Mbps
                                # "-vf", "scale=480:trunc(ow/a/2)*2", #Will Figure out how this works later
                                "-hls_list_size", "0",
                                "-f", "flv",
                                "rtmp://10.0.0.19/hls/stream_high",  # Destination URL for streaming
                                
                                #Higher Quality Stream
                                
                                "-c:v", "h264_nvenc",  # Video codec: h264 using NVENC encoder
                                "-map", "0:0",
                                "-map", f"0:{audio_stream}",  # Selects the the English audio
                                "-map", f"0:{subtitle_stream}?",
                                "-c:a", "aac",  # Audio codec: aac
                                "-ac", "2",     # Audio channels: 2
                                "-ar", "22050",  # Audio sample rate: 22050 Hz
                                "-b:v", "1920k",      # Video bitrate: 5 Mbps
                                # "-vf", "scale=480:trunc(ow/a/2)*2", #Will Figure out how this works later
                                "-hls_list_size", "0",
                                "-f", "flv",
                                "rtmp://10.0.0.19/hls/stream_higher`",  # Destination URL for streaming

                                #Source Quality Stream
                                
                                "-c:v", "h264_nvenc",  # Video codec: h264 using NVENC encoder
                                "-map", "0:0",
                                "-map", f"0:{audio_stream}",  # Selects the the English audio
                                "-map", f"0:{subtitle_stream}?",
                                "-c:a", "aac",  # Audio codec: aac
                                "-ac", "2",     # Audio channels: 2
                                "-ar", "22050",  # Audio sample rate: 22050 Hz
                                "-b:v", "10M",      # Video bitrate: 5 Mbps
                                # "-vf", "scale=480:trunc(ow/a/2)*2", #Will Figure out how this works later
                                "-hls_list_size", "0",
                                "-f", "flv",
                                "rtmp://10.0.0.19/hls/stream_src"  # Destination URL for streaming
                            ]
            print(ffmpeg_command)
            print(f"Notice: Playing \"{filename}\" with Audio stream \"{audio_stream}\".")
            ffmpeg_result = subprocess.run(ffmpeg_command, capture_output=True)
            ffmpeg_output = ffmpeg_result.stderr.decode("utf-8")
            print(ffmpeg_output)
            if "Server error: Already publishing" not in ffmpeg_output:
                return True
            else:
                print("Error: Stream already publishing. Retrying in 5 seconds.")
                # time.sleep(2)
                return False
        else:
            return True
