from glob import iglob
import os
import sys
from typing import List
from PIL import Image
from reportlab.pdfgen import canvas
from progress.bar import IncrementalBar
from collections import namedtuple

# ------------------------------------------------------------------------------

FILES_SORT_KEY = lambda x: int(os.path.basename(x).split(".")[0])
FILES_FIND_PATH = "%s/Chapter №%d/*.[jp][pn]g"
ChapterInfo = namedtuple("ChapterInfo", ["num", "images"])

# ------------------------------------------------------------------------------

def create_pdf(manga, manga_path: str, fname: str, volume_num: int):
    """Creates the .pdf file from volume's chapters"""
    chapter_numbers = manga.volumes[volume_num]
    chapter_list = []

    # Getting images to compile into .pdf
    for ch_num in chapter_numbers:
        ch_path = FILES_FIND_PATH % (manga_path, ch_num)
        ch = ChapterInfo(ch_num, sorted(iglob(ch_path), key=FILES_SORT_KEY))
        if len(ch.images) == 0: continue
        chapter_list.append(ch)

    # If the volume has not been loaded
    if len(chapter_list) == 0: return

    canv = canvas.Canvas(fname)
    text = f"Creating .pdf from {volume_num} vol..."
    bar = IncrementalBar(text, max=sum(len(x.images) for x in chapter_list))

    for chapter in chapter_list:
        for page in chapter.images:
            # If page is first in the list
            if page == chapter.images[0]: 
                key = str(chapter.num)
                canv.bookmarkPage(key)
                canv.addOutlineEntry(f"Глава {chapter.num}", key)
            # Getting the image size
            img = Image.open(page)
            canv.setPageSize((img.width, img.height))
            canv.drawImage(page, 0, 0)
            canv.showPage()
            bar.next()
    bar.finish()
    canv.save()
