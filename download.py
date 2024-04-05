import os
import re
import json
from pprint import pprint
from dateutil.parser import parse
# import youtube_dl
try:
    import yt_dlp as youtube_dl
    import googleapiclient.discovery
except:
    #install with pip
    os.system("pip install --upgrade google-api-python-client")
    os.system("pip install --upgrade yt_dlp")
    import yt_dlp as youtube_dl
    import googleapiclient.discovery

class Downloader:
    def __init__(self):
        self.videoInfo = []
        self.DEVELOPER_KEY = "API_KEY"
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, developerKey=self.DEVELOPER_KEY)
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(os.getcwd(), "temp", "%(title)s.%(ext)s"),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '96',
            }],
        }

    def ISO8601_to_min(self, s):
        duration = parse(s[2:]).strftime("%H:%M:%S")
        return duration

    def getVideoInfo(self, url):
        pattern = r'(?:https?:\/{2})?(?:w{3}\.)?youtu(?:be)?\.(?:com|be)(?:\/watch\?v=|\/)([^\s&]+).*'
        if (match := re.match(pattern, url)):
            videoId = match.group(1)
        else:
            print("O argumento não corresponde com uma URL válida.")
            print("Finalizando a execução.")
            exit()

        request = self.youtube.videos().list(
                    part="contentDetails,snippet",
                    id=videoId
                )
        vidresponse = request.execute()["items"][0]
        title = vidresponse["snippet"]["title"]
        duration = self.ISO8601_to_min(vidresponse["contentDetails"]["duration"])
        description = vidresponse["snippet"]["description"]
        vidFormat = ""
        return (title, duration, description)

    def downloadVideo(self, url):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])
