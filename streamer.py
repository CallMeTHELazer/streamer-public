from random import shuffle
import random
import argparse
import tools.jsoner as jsoner
import time
import ffmpeg_player

parser = argparse.ArgumentParser(description="Runs a stream poined at a webserver")
parser.add_argument("-s", "--series_file", action="store", dest="series_file",
                    type=str,help="Input series File")
parser.add_argument("-m", "--movies_file", action="store", dest="movies_file",
                    type=str,help="Input Movie File")
parser.add_argument("-o", "--override", action="store", dest="override_file",
                    type=str, help="Start with a file you want.")
parser.add_argument("-y", "--youtube", action="store", dest="youtube_file",
                    type=str, help="Input Youtube File.")
parser.add_argument("--shuffle", action="store_true", dest="shuffle",
                    help="Enable shuffling of files (default: False)")
parser.add_argument("--dry", action="store_true", dest="dry",
                    help="Enable shuffling of files (default: False)")
args = parser.parse_args()

json_movie_file = args.movies_file
json_series_file= args.series_file
json_youtube_file= args.youtube_file
json_bumps_file= "json_bumps.json"
json_shuffled_movies_file = "~/streamer-public/json_shuffled_movies.json"
json_shuffled_series_file = "~/streamer-public/json_shuffled_series.json"
json_shuffled_bumps_file = "~/streamer-public/json_shuffled_bumps.json"
json_shuffled_youtube_file = "~/streamer-public/json_shuffled_youtube.json"
# json_shuffled_movies_file = "json_shuffled_movies.json"
# json_shuffled_series_file = "json_shuffled_series.json"
# json_shuffled_bumps_file = "json_shuffled_bumps.json"
# json_shuffled_youtube_file = "json_shuffled_youtube.json"

kill_var = True

def shuffle_files(json_file,media_type):

    files = jsoner.loader(json_file,"filenames")

    shuffle(files)

    jsoner.creator(files,"shuffled_"+media_type,"filenames")
    return files


def play_random_media():
    """Plays a random media file from the specified media type."""
    media_type = ""
    choices = []
    if args.series_file is not None:
        choices.append("series")
        movies = jsoner.loader(json_shuffled_movies_file,"filenames")
    if args.movies_file is not None:
        choices.append("movies")
        series = jsoner.loader(json_shuffled_series_file,"filenames")
    if args.youtube_file is not None:
        choices.append("youtube")
        youtube = jsoner.loader(json_shuffled_youtube_file,"filenames")

    media_type = random.choice(choices)

    played_successful = False
    

    if media_type == "series" and args.series_file is not None:
        # Use appropriate shuffled series filename (e.g., json_shuffled_series.json)
        for i, filename in enumerate(series):
            while played_successful is not True:
                played_successful = ffmpeg_player.player(filename, args.dry)
                if played_successful:
                    del series[i]
                    jsoner.creator(series,"shuffled_"+media_type,"filenames")
                    break
        return True
    elif media_type == "movies" and args.movies_file is not None:
        # Use appropriate shuffled movie filename (e.g., json_shuffled_movies.json)
        for i, filename in enumerate(movies):
            while played_successful is not True:
                played_successful = ffmpeg_player.player(filename, args.dry)
                if played_successful:
                    del movies[i]
                    jsoner.creator(movies,"shuffled_"+media_type,"filenames")
                    break
        return True
    elif media_type == "youtube" and args.youtube_file is not None:
        # Use appropriate shuffled Youtube filename (e.g., json_shuffled_Youtube.json)
        for i, filename in enumerate(youtube):
            while played_successful is not True:
                played_successful = ffmpeg_player.player(filename, args.dry)
                if played_successful:
                    del youtube[i]
                    jsoner.creator(youtube,"shuffled_"+media_type,"filenames")
                    break
        return True
    else:
        print(f"No {media_type} file provided or both arguments were specified.")
        return False


if __name__ == "__main__":
    

    if args.override_file != None:
        
        played_successful = False
        override_file = args.override_file
        print(f"Override Found. Playing File: "+override_file)
        while played_successful is not True:
            played_successful = ffmpeg_player.player(override_file,args.dry)

    if args.series_file is not None or args.movies_file is not None:

        if args.series_file != None:
            print(f"Series File Found.")
            if args.shuffle is True:
                shuffle_files(json_series_file,"series")
        if args.movies_file != None:
            print(f"Movies File Found.")
            if args.shuffle is True:
                shuffle_files(json_movie_file,"movies")
        if args.youtube_file != None:
            print(f"Youtube File Found.")
            if args.shuffle is True:
                shuffle_files(json_youtube_file,"youtube")

        while kill_var is True:
            kill_var = play_random_media()
            movies_left = jsoner.counter(json_shuffled_movies_file,"filenames")
            if movies_left < 1:
                break
            # time.sleep(11)

    else:
        print("No ARGS supplied, please add arguments in '-s=""/path/to/series/json""'")
    
