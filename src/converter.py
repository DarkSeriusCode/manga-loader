from glob import iglob
import os
import sys
from typing import List
from PIL import Image
from reportlab.pdfgen import canvas
from progress.bar import IncrementalBar

# ------------------------------------------------------------------------------

FILES_SORT_KEY = lambda x: int(os.path.basename(x).split(".")[0])
FILES_FIND_PATH = "%s/Chapter №%d/*.[jp][pn]g"

# ------------------------------------------------------------------------------

def create_pdf(manga, manga_path: str, fname: str, volume_num: int):
    """Creates the .pdf file from volume's chapters"""
    chapter_numbers = manga.volumes[volume_num]
    files = []

    # Getting images to compile into .pdf
    for ch_num in chapter_numbers:
        files_iter = iglob(FILES_FIND_PATH % (manga_path, ch_num))
        files.extend(sorted(files_iter, key=FILES_SORT_KEY))
        # Adding a empty page
        if len(files) > 0: files.append(None)

    # If the volume has not been loaded
    if len(files) == 0: return

    canv = canvas.Canvas(fname)
    bar = IncrementalBar(f"Creating .pdf from {volume_num} vol", max=len(files))

    for file_num, file in enumerate(files, 0):
        if file:
            # Getting the image size
            img = Image.open(file)
            size = (img.width, img.height)
            canv.setPageSize(size)
            canv.drawImage(file, 0, 0)
        else:
            canv.setPageSize((size[0], 10))
        canv.showPage()
        bar.next()
    bar.finish()
    canv.save()