import os
import random
import string
from shutil import copyfile
import xml.etree.ElementTree as ET
from email.utils import formatdate

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class Feed:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.pubDate = ""
        self.enclosure_url = ""
        self.length = 0
        self.duration = ""
        self.guid = ""     

    def createRSS(self, rssLayoutPath, rssFilePath):
        print("Criando arquivo RSS")
        print(f"Criando rss em {rssFilePath}")
        copyfile(rssLayoutPath, rssFilePath)

    def rguid(self):
        rdn = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
        return rdn

    def addEpisode(self, rssFilePath, title, duration, description, length, fileLink):
        print("Adicionando Episódio ao rss")
        self.tree = ET.parse(rssFilePath)
        self.root = self.tree.getroot()
        self.channel = self.root[0]
        self.item = ET.Element("item")
        self.title = ET.SubElement(self.item, "title")
        self.title.text = title
        self.description = ET.SubElement(self.item, "description")
        self.description.text = description
        self.pubDate = ET.SubElement(self.item, "pubDate")
        self.pubDate.text = formatdate()
        self.enclosure_url = ET.SubElement(self.item, "enclosure", attrib={
            "url": fileLink,
            "type": "audio/mpeg",
            "length": length
        })
        self.duration = ET.SubElement(self.item, "duration")
        self.duration.text = duration
        self.guid = ET.SubElement(self.item, "guid")
        self.guid.text = self.rguid()
        self.root[0].insert(6,self.item)
        indent(self.root)
        self.tree.write(open(rssFilePath, "wb"))