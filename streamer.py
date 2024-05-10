from random import shuffle, choice
# import random
import argparse
import tools.jsoner as jsoner
# import time
import ffmpeg_player

parser = argparse.ArgumentParser(description="Runs a stream poined at a webserver")

parser.add_argument("-s", "--series_file", action="store_true", dest="series_file",
                    help="Input series File")

parser.add_argument("-m", "--movies_file", action="store_true", dest="movies_file",
                    help="Input Movie File")

parser.add_argument("-y", "--youtube", action="store_true", dest="youtube_file",
                    help="Input Youtube File.")

parser.add_argument("-o", "--override", action="store", dest="override_file",
                    type=str, help="Start with a file you want.")

parser.add_argument("--shuffle", action="store_true", dest="shuffle",
                    help="Enable shuffling of files (default: False)")

parser.add_argument("--dry", action="store_true", dest="dry",
                    help="Enable shuffling of files (default: False)")

args = parser.parse_args()

json_movie_file = args.movies_file
json_series_file= args.series_file
json_youtube_file= args.youtube_file
# json_bumps_file= "json_bumps.json"

json_directory_file = "/home/pokeruadmin/streamer-public/json_directory.json"
json_shuffled_directory_file = "/home/pokeruadmin/streamer-public/json_shuffled_directory.json"
# json_directory_file = "json_directory.json"
# json_shuffled_directory_file = "json_shuffled_directory.json"


kill_var = True

def shuffle_files(json_file,media_type):

    files = jsoner.loader(json_file,media_type)

    shuffle(files)

    jsoner.creator(files,json_shuffled_directory_file,media_type)
    return files


def play_random_media():
    """Plays a random media file from the specified media type."""
    media_type = ""
    choices = []
    if args.series_file is True:
        choices.append("series")
        series = jsoner.loader(json_shuffled_directory_file,"series")
    if args.movies_file is True:
        choices.append("movies")
        movies = jsoner.loader(json_shuffled_directory_file,"movies")
    if args.youtube_file is True:
        choices.append("youtube")
        youtube = jsoner.loader(json_shuffled_directory_file,"youtube")

    media_type = choice(choices)

    played_successful = False
    

    if media_type == "series" and args.series_file is True:
        # Use appropriate shuffled series filename (e.g., json_shuffled_series.json)
        for i, filename in enumerate(series):
            while played_successful is not True:
                played_successful = ffmpeg_player.player(filename, args.dry)
                if played_successful:
                    del series[i]
                    combined = {"series": series, "movies": movies, "youtube": youtube}
                    jsoner.creator(combined,json_shuffled_directory_file)
                    # jsoner.creator(series,json_shuffled_directory_file,"series")
                    break
        return True
    elif media_type == "movies" and args.movies_file is True:
        # Use appropriate shuffled movie filename (e.g., json_shuffled_movies.json)
        for i, filename in enumerate(movies):
            while played_successful is not True:
                played_successful = ffmpeg_player.player(filename, args.dry)
                if played_successful:
                    del movies[i]
                    combined = {"series": series, "movies": movies, "youtube": youtube}
                    jsoner.creator(combined,json_shuffled_directory_file)
                    # jsoner.creator(movies,json_shuffled_directory_file,"movies")
                    break
        return True
    elif media_type == "youtube" and args.youtube_file is True:
        # Use appropriate shuffled Youtube filename (e.g., json_shuffled_Youtube.json)
        for i, filename in enumerate(youtube):
            while played_successful is not True:
                played_successful = ffmpeg_player.player(filename, args.dry)
                if played_successful:
                    del youtube[i]
                    combined = {"series": series, "movies": movies, "youtube": youtube}
                    jsoner.creator(combined,json_shuffled_directory_file)
                    # jsoner.creator(youtube,json_shuffled_directory_file,"youtube")
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

        movies = jsoner.loader(json_directory_file,"movies")
        series = jsoner.loader(json_directory_file,"series")
        youtube = jsoner.loader(json_directory_file,"youtube")

        if args.shuffle is True:
            if args.series_file is True:
                print(f"Series File Found.")
                shuffle(series)
            if args.movies_file is True:
                print(f"Movies File Found.")
                shuffle(movies)
            if args.shuffle is True:
                print(f"Youtube File Found.")
                shuffle(youtube)
            combined = {"series": series, "movies": movies, "youtube": youtube}

            jsoner.creator(combined,json_shuffled_directory_file)
            # print(combined)
        
        


        # if args.series_file is True:
        #     print(f"Series File Found.")
        #     if args.shuffle is True:
        #         shuffle_files(json_directory_file,"series")
        # if args.movies_file is True:
        #     print(f"Movies File Found.")
        #     if args.shuffle is True:
        #         shuffle_files(json_directory_file,"movies")
        # if args.youtube_file is True:
        #     print(f"Youtube File Found.")
        #     if args.shuffle is True:
        #         shuffle_files(json_directory_file,"youtube")

        while kill_var is True:
            kill_var = play_random_media()
            movies_left = jsoner.counter(json_shuffled_directory_file,"movies")
            if movies_left < 1:
                break
            # time.sleep(11)

    else:
        print("No ARGS supplied, please add arguments in '-s=""/path/to/series/json""'")
    
