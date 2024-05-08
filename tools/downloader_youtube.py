from pytube import YouTube,Channel,Playlist
import jsoner as jsoner
import argparse

parser = argparse.ArgumentParser(description="Downloads YouTube Videos or Channels.")
parser.add_argument("-s", "--source", action="store", dest="source", required=True,
                    type=str,help="Input Source as a link or JSON List File. (JSON LIST FILE REQUIRES ARGUMENT -m)")
parser.add_argument("-d", "--destination_file", action="store", dest="destination_file", required=True,
                    type=str,help="Input Output File")
parser.add_argument("-c", "--channel", action="store_true", dest="channel",
                    help="Use this if the input file is a channel (default: False)")
parser.add_argument("-m", "--multiple", action="store_true", dest="multiple",
                    help="Enable multiple video list (default: False)")
parser.add_argument("-p", "--playlist", action="store_true", dest="playlist",
                    help="Use if this is a playlist. (default: False)")
args = parser.parse_args()

source_file = args.source
output_directory = args.destination_file

if args.multiple is True:
    video_links = jsoner.loader(source_file,"filenames")
else:
    video_links = source_file

def download_youtube_videos(video_links, output_directory):

    if args.channel is False and args.playlist is False:
        for video_link in video_links:
            try:
                video = YouTube(video_link)
                video_filename = video.title+".mp4"
            except:
                print(f"Could Not Resolve Title of "+video_link)
            try:
                video.streams.first().download(output_directory,video_filename)
                print(f"Downloaded Video "+video_filename)
            except:
                print(f"Could Not Download Video, Trying a different way.")
                video_link = video_link+"&feature=youtu.be"
                try:
                    video = YouTube(video_link)
                    video.streams.filter(file_extension='mp4').first().download(output_directory,video_filename)
                    print(f"Downloaded Video "+video_filename)
                except:
                    print("That didnt work either, The video is probabby private. "+video_link)
    if args.channel is True and args.playlist is False:
        c = Channel(video_links)
        try:

            print(f'Downloading videos by: {c.channel_name}')
            for video in c.videos:
                video.streams.first().download(output_directory)
        except:
            print("That didnt work either, The video is probabby private. ")
    
    if args.channel is False and args.playlist is True:
        p = Playlist(video_links)
        try:
            print(f'Downloading videos by: {p.title}')
            for video in p.videos:
                try:
                    video.streams.filter(file_extension='mp4').first().download(output_directory)
                except:
                    print(f"Could Not Download Video")
            # for url in p.video_urls[:30]:
            #     print(url)
        except:
            print("That didnt work either, The video is probabby private. ")
            # try:
            #     video = YouTube(url)
            #     video_filename = video.title+".mp4"
            # except:
            #     print(f"Could Not Resolve Title of "+video_link)
            # try:
            #     video.streams.first().download(output_directory,video_filename)
            #     print(f"Downloaded Video "+video_filename)
            # except:
            #     print(f"Could Not Download Video, Trying a different way.")
            #     video_link = video_link+"&feature=youtu.be"


download_youtube_videos(video_links, output_directory)