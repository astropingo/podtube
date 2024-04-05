import os
import download
import updaterss
import sendtodropbox
import filemanager
from pprint import pprint
import shutil
import sys

url = sys.argv[1]
rssFolderName = "rss"
rssName = "rss.rss"
rssLayoutName = "rssLayout.xml"
tempFolder = os.path.join(os.getcwd(), "temp")
rssFilePath = os.path.join(os.getcwd(), rssFolderName, rssName)
rssLayoutPath = os.path.join(os.getcwd(), rssFolderName, rssLayoutName)

dl = download.Downloader()
title, duration, description = dl.getVideoInfo(url)
fileLength = 0

print(f"Fazendo download do vídeo \"{title}\"...")
dl.downloadVideo(url)
print(f"Vídeo \"{title}\" salvo com sucesso!")

dbx = sendtodropbox.DBXDownloader()
rss = updaterss.Feed()

for files in os.listdir(tempFolder):
    print(tempFolder)
    fileName = os.path.split(files)[1]
    filePath = os.path.join(tempFolder, fileName)
    print(f"Fazendo upload do arquivo {fileName}")
    fileLength = os.path.getsize(filePath)
    if fileLength >= 1.5e+8:
        print(f"O tamanho do arquivo {fileName} ({fileLength}) excede o máximo permitido (150 MB) e não pode ser enviado.")
    else:
        dbx.upload(filePath, dbxUploadFolder="audio")
        fileLink = dbx.getShareLink()

    if "rss.rss" not in os.listdir(os.path.join(os.getcwd(), rssFolderName)):
        rss.createRSS(rssLayoutPath, rssFilePath)
    rss.addEpisode(rssFilePath, title, duration, description, str(0), fileLink)
    dbx.upload(rssFilePath, dbxUploadFolder="rss")

shutil.rmtree(tempFolder)