#This file does not work, Just leaving it here for now

from vimeo_downloader import Vimeo

def download_vimeo_videos(video_links, output_directory):
  """Downloads Vimeo videos from a list of links and saves them to a directory.

  Args:
    video_links: A list of Vimeo video URLs.
    output_directory: The directory where the downloaded videos will be saved.
  """
  for video_link in video_links:
    try:
      v = Vimeo(video_link)
      meta = v.metadata
      print("Title is "+str(meta.title))
      print(f"Link Validated "+video_link)
      filename_video = str(meta.title)+".mp4"
      id = meta.id
      # print(id)
    except:
      print(f"Parsing to Video, Please Check the link and try again. : {video_link}")
    
    try:
      s = v.streams
      print(s)
      best_stream = s[-1] #Selcts the best stream.
      print("Filesize is "+str(best_stream))
      best_stream.download(output_directory, filename_video)
    except:
      print(f"Error downloading could not find correct stream, trying from video ID. : {video_link}")
      try:
        v = Vimeo.from_video_id(str(id))
        print(id)
        s = v.streams
        print(s)
        best_stream = s[-1] #Selcts the best stream.
        print("Filesize is "+str(best_stream))
        best_stream.download(output_directory, filename_video)
      except:
        print("Broke again, trying vimeo_dl")

# Example usage
video_links = [
  "https://vimeo.com/146074548"
]
output_directory = "videos_vimeo"

download_vimeo_videos(video_links, output_directory)