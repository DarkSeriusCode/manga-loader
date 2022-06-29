import os
import re
import shutil
import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from typing import Dict, List

# ------------------------------------------------------------------------------

REQUEST_HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
}

# ------------------------------------------------------------------------------

class ParserException(Exception):
    def __init__ (self, text):
        self.text = f"\033[31m{text}\033[0m"
        super().__init__(self.text)

# ------------------------------------------------------------------------------

class Chapter:
    link_regexpr = re.compile(r"https://h\d+.?\.rmr\.rocks/auto(/\d+){3}/[^\[\]]+(jpg|png)\?t=\d+&u=\d+&h=\S{22}")
    def __init__ (self, url: str, count: int, volume: int):
        self.url = url
        self.volume = volume
        self.count = count

        # mtr=1 is needed for get adult content
        html = requests.get(url + "?mtr=1", headers=REQUEST_HEADER).text
        parser = BeautifulSoup(html, "html.parser")
        self.name = parser.find("h1").text.strip()

        # Getting a list of links using the JS code processing
        script = parser.findAll("script", {"type": "text/javascript"})[8]
        script = str(script).split("\n")[5]
        for x in [",", "'", "\""]:
            script = script.replace(x, "")
            
        self.links = [x.group(0) for x in re.finditer(self.link_regexpr, script)]
        # The number of pages
        self.size = len(self.links)

    def download (self, path: str="./"):
        """Loads chapter as group of images"""
        load_path = f"{path}/Chapter №{self.count}/"
        bar = IncrementalBar(f"Loading chapter {self.count}", max=self.size)
        os.makedirs(load_path, exist_ok=True)

        for num, link in enumerate(self.links, 1):
            response = requests.get(link, stream=True)
            ext = link.split(".")[-1].split("?")[0]
            if response.status_code == 200:
                with open(f"{load_path}{num}.{ext}", "wb") as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f) 
            bar.next()
        bar.finish()

# ------------------------------------------------------------------------------

class Manga:
    SUPPORTED_DOMAINS = ["https://readmanga.live", "https://mintmanga.live", 
                         "https://readmanga.io"]
    def __init__ (self, url: str):
        self.url = url
        self.chapters = []
        self.chapters_names = []

        try:
            resp = requests.get(url, headers=REQUEST_HEADER)
            if resp.status_code != 200: 
                raise ParserException(f"Incorrect server response ({resp.status_code})")
        except requests.exceptions:
            raise ParserException("Cannot send a request to the server!")
        self.parser = BeautifulSoup(resp.text, "html.parser")

        # Is there adult content in the manga
        self.is_mtr = bool(self.parser.find("div", {"class": "mtr-message"}))

        try:
            # Getting manga name
            self.name = self.parser.find("meta", {"itemprop": "name"}).attrs["content"]
        except AttributeError:
            raise ParserException("The URL is incorrect")

        # Getting the domain and checking it for validity
        self.domain = "https://" + url.split("/")[2]
        if self.domain not in self.SUPPORTED_DOMAINS: 
            raise ParserException(self.domain + " is unsupported domain!")

        # Getting a chapter links and their number
        self.chapters_links = self.get_chapters_links()
        self.ch_count = len(self.chapters_links)
        self.vol_count = self.__get_volume_from_link(self.chapters_links[-1])
        self.volumes = self.get_volumes()

    def get_volumes(self) -> Dict[int, List[int]]:
        """Returns a dict containing the number of each chapter in the volume""" 
        volumes = {}
        for ch_num, link in enumerate(self.chapters_links, 1):
            vol_num = self.__get_volume_from_link(link)
            volumes.setdefault(vol_num, [])
            volumes[vol_num].append(ch_num)
        return volumes

    def __get_volume_from_link(self, link: str) -> int:
        """Gets the volume number from URL"""
        return int(link.split("/")[-2].replace("vol", ""))

    def get_chapters_links (self) -> List[Chapter]:
        """Gets manga chapters"""
        tag_class = "chapter-link cp-l manga-mtr" if self.is_mtr else "chapter-link cp-l"
        tags = self.parser.findAll("a", {"class": tag_class})
        links = []
        for tag in tags:
            links.append(self.domain + tag.attrs["href"])
        return links[::-1]    

    def chapters_iter(self, start: int, end: int):
        """Generator that creates a Chapter objects in range [start;end]"""
        for num in range(start, end + 1):
            chapter_link = self.chapters_links[num - 1]
            chapter_volume = self.__get_volume_from_link(chapter_link)
            chapter = Chapter(chapter_link, num, chapter_volume)
            yield chapter

    def download(self, start: int, end: int, path: str="./"):
        """Loads the chapters from start to end. Where start and end are the 
        chapter numbers. NOT indexes in list!"""
        for chapter in self.chapters_iter(start, end):
            chapter.download(path)