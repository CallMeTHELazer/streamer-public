import os
import argparse
import jsoner

# Define video extensions
video_extensions = ["mp4", "avi", "mkv"]
directory_series = ["/HDD_1/plexmedia/series", "/HDD_2/plexmedia/series"]
directory_movies = ["/HDD_1/plexmedia/movies", "/HDD_2/plexmedia/movies"]
directory_bumps = ["/home/pokeruadmin/streamer/bumps"]
directory_youtube = ["/HDD_2/videos"]

movies = []
series = []
youtube = []
bumps = []

def creator_series(series):
    if series is True:
        print("Series Requested. Gathering Series filenames.")
        # Loop through target directories
        files = walker(directory_series)
        return files
        jsoner.creator(files,"json_directory.json","series")
    else:
       print("Series Not Selected, please use '--series' if you want to search through the series.")

def creator_movies(movies):
    if movies is True:
        print("Movies Requested. Gathering Movies filenames.")
        # Loop through target directories
        files = walker(directory_movies)
        return files
        jsoner.creator(files,"json_directory.json","movies")
    else:
       print("Movies Not Selected, please use '--movies' if you want to search through the movies.")

def creator_bumps(bumps):
    if bumps is True:
        print("Bumps Requested. Gathering Bumps filenames.")
        # Loop through target directories
        files = walker(directory_bumps)
        return files
        jsoner.creator(files,"json_directory.json","bumps")
    else:
       print("Bumps Not Selected, please use '--bumps' if you want to search through the bumps.")

def creator_youtube(youtube):
    if youtube is True:
        print("Youtube Requested. Gathering Bumps filenames.")
        # Loop through target directories
        files = walker(directory_youtube)
        return files
        jsoner.creator(files,"json_directory.json","movies")
    else:
       print("Youtube Not Selected, please use '--youtube' if you want to search through the youtube.")

def walker(directory_search):
    all_filenames = []
    print("Walking Through Directories")
    for directory in directory_search:
    # Check if directory exists
        if os.path.isdir(directory):
            # Walk through the directory structure
            for root, _, files in os.walk(directory):
                for filename in files:
                    # Check for matching extensions
                    if filename.lower().endswith(tuple(f".{ext}" for ext in video_extensions)):
                        # Build full path
                        full_path = os.path.join(root, filename)
                        # Append to list
                        all_filenames.append(full_path)
        else:
            print(f"Directory '{directory}' does not exist. Skipping...")
        return all_filenames


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse through Bumps, Movies, and Series")
    parser.add_argument("-s", "--series", action="store_true", dest="series",
                        help="Enable series mode (default: False)")
    parser.add_argument("-m", "--movies", action="store_true", dest="movies",
                        help="Enable movies mode (default: False)")
    parser.add_argument("-b", "--bumps", action="store_true", dest="bumps",
                        help="Enable Bumps mode (default: False)")
    parser.add_argument("-y", "--youtube", action="store_true", dest="youtube",
                        help="Enable YouTube mode (default: False)")
    args = parser.parse_args()
    movies = creator_movies(args.movies)
    series = creator_series(args.series)
    bumps = creator_bumps(args.bumps)
    youtube = creator_youtube(args.youtube)
    combined = {"series": series, "movies": movies, "youtube": youtube, "bumps": bumps}

    jsoner.creator(combined,"json_directory.json")