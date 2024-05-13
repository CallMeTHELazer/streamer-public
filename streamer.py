from random import shuffle, choice  # Importing shuffle and choice functions from random module
import argparse  # Importing argparse for parsing command-line arguments
import tools.jsoner as jsoner  # Importing a module named jsoner from tools package
import ffmpeg_player  # Importing ffmpeg_player module
import logging
import config_logging

#Logging Configurarion
logger = logging.getLogger(__name__)
log_level = getattr(logging, config_logging.logging_level.upper())
logging.basicConfig(level=log_level)
# logger.setLevel(logging.config_logging.logging_level)
file_handler = logging.FileHandler(config_logging.logging_file)
logger.addHandler(file_handler)

# Creating an argument parser object
parser = argparse.ArgumentParser(description="Runs a stream pointed at a webserver")

# Adding arguments to the parser
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

# Parsing the command-line arguments
args = parser.parse_args()

# Assigning values of command-line arguments to variables
json_movie_file = args.movies_file
json_series_file = args.series_file
json_youtube_file = args.youtube_file

# Defining file paths for JSON files
json_directory_file = "/home/pokeruadmin/streamer-public/json_directory.json"
json_shuffled_directory_file = "/home/pokeruadmin/streamer-public/json_shuffled_directory.json"
# json_directory_file = "json_directory.json"
# json_shuffled_directory_file = "json_shuffled_directory.json"

# Initializing a variable
kill_var = True

# Function to shuffle files
def shuffle_files(json_file, media_type):
    files = jsoner.loader(json_file, media_type)  # Loading files from JSON
    shuffle(files)  # Shuffling files
    jsoner.creator(files, json_shuffled_directory_file, media_type)  # Creating JSON with shuffled files
    return files

# Function to play random media file
def play_random_media():
    choices = []  # Initializing a list for media types
    if args.series_file:  # If series file option is provided
        choices.append("series")  # Add series to choices
        series = jsoner.loader(json_shuffled_directory_file, "series")  # Load shuffled series
    if args.movies_file:  # If movies file option is provided
        choices.append("movies")  # Add movies to choices
        choices.append("movies")  # Add movies to choices
        movies = jsoner.loader(json_shuffled_directory_file, "movies")  # Load shuffled movies
    if args.youtube_file:  # If YouTube file option is provided
        choices.append("youtube")  # Add YouTube to choices
        youtube = jsoner.loader(json_shuffled_directory_file, "youtube")  # Load shuffled YouTube videos

    media_type = choice(choices)  # Choose a random media type
    played_successful = False  # Initializing a variable

    if media_type == "series" and args.series_file:  # If media type is series and series file option is provided
        for i, filename in enumerate(series):  # Iterate over series filenames
            while not played_successful:  # While played not successful
                logger.info(f"Playing Filename "+filename)
                played_successful = ffmpeg_player.player(filename, args.dry)  # Play the media
                if played_successful:
                    logger.info(filename+" Played Successful.")
                    del series[i]  # Delete played file from series
                    combined = {"series": series, "movies": movies, "youtube": youtube}  # Combined media
                    jsoner.creator(combined, json_shuffled_directory_file)  # Create JSON with updated media
                    break  # Break the loop
        return True  # Return True if played successfully
    elif media_type == "movies" and args.movies_file:  # If media type is movies and movies file option is provided
        for i, filename in enumerate(movies):  # Iterate over movies filenames
            while not played_successful:  # While played not successful
                logger.info(f"Playing Filename "+filename)
                played_successful = ffmpeg_player.player(filename, args.dry)  # Play the media
                if played_successful:
                    logger.info(filename+" Played Successful.")
                    del movies[i]  # Delete played file from movies
                    combined = {"series": series, "movies": movies, "youtube": youtube}  # Combined media
                    jsoner.creator(combined, json_shuffled_directory_file)  # Create JSON with updated media
                    break  # Break the loop
        return True  # Return True if played successfully
    elif media_type == "youtube" and args.youtube_file:  # If media type is YouTube and YouTube file option is provided
        for i, filename in enumerate(youtube):  # Iterate over YouTube filenames
            while not played_successful:  # While played not successful
                logger.info(f"Playing Filename "+filename)
                played_successful = ffmpeg_player.player(filename, args.dry)  # Play the media
                if played_successful:
                    logger.info(filename+" Played Successful.")
                    del youtube[i]  # Delete played file from YouTube
                    combined = {"series": series, "movies": movies, "youtube": youtube}  # Combined media
                    jsoner.creator(combined, json_shuffled_directory_file)  # Create JSON with updated media
                    break  # Break the loop
        return True  # Return True if played successfully
    else:
        logger.critical(f"No {media_type} file provided or both arguments were specified.")
        return False  # Return False if media type not provided or arguments not specified

# Main execution
if __name__ == "__main__":
    if args.override_file:  # If override file is provided
        played_successful = False  # Initializing a variable
        override_file = args.override_file  # Override file
        logger.info(f"Override Found. Playing File: " + override_file)  # Print override file
        while not played_successful:  # While played not successful
            played_successful = ffmpeg_player.player(override_file, args.dry)  # Play the media

    if args.series_file or args.movies_file:  # If series or movies file options provided
        movies = jsoner.loader(json_directory_file, "movies")  # Load movies
        series = jsoner.loader(json_directory_file, "series")  # Load series
        youtube = jsoner.loader(json_directory_file, "youtube")  # Load YouTube videos

        if args.shuffle:  # If shuffle option provided
            if args.series_file:  # If series file option provided
                logger.info(f"Series File Found.")  # Print series file found
                shuffle(series)  # Shuffle series
            if args.movies_file:  # If movies file option provided
                logger.info(f"Movies File Found.")  # Print movies file found
                shuffle(movies)  # Shuffle movies
            if args.youtube_file:  # If YouTube file option provided
                logger.info(f"Youtube File Found.")  # Print YouTube file found
                shuffle(youtube)  # Shuffle YouTube videos
            combined = {"series": series, "movies": movies, "youtube": youtube}  # Combined media
            jsoner.creator(combined, json_shuffled_directory_file)

        while kill_var is True:
            kill_var = play_random_media()
            movies_left = jsoner.counter(json_shuffled_directory_file,"movies")
            youtube_left = jsoner.counter(json_shuffled_directory_file,"youtube")
            series_left = jsoner.counter(json_shuffled_directory_file,"series")
            if movies_left < 1:
                logger.info(f"Movies List Exhausted, Shuffling Movies")
                shuffle(movies)  # Shuffle movies
                combined = {"series": series, "movies": movies, "youtube": youtube}  # Combined media
                jsoner.creator(combined, json_shuffled_directory_file)
            if series_left < 1:
                logger.info(f"Series List Exhausted, shuffleing Series.")
                shuffle(series)  # Shuffle series
                combined = {"series": series, "movies": movies, "youtube": youtube}  # Combined media
                jsoner.creator(combined, json_shuffled_directory_file)
            if youtube_left < 1:
                logger.info(f"Youtube List Exhausted, Shuffleing Youtube.")
                shuffle(youtube)  # Shuffle YouTube videos
                combined = {"series": series, "movies": movies, "youtube": youtube}  # Combined media
                jsoner.creator(combined, json_shuffled_directory_file)
            # time.sleep(11)

    else:
        print("No ARGS supplied, please add arguments in '-s=""/path/to/series/json""'")
    
