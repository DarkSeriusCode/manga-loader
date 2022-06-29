import argparse
import sys
from src import parser
from src.pretty_console_logs import *
from src.converter import create_pdf

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("url")
    argparser.add_argument("-s", type=int, dest="start", 
        help="The number of the first chapter for download")
    argparser.add_argument("-e", type=int, dest="end", 
        help="The number of the last chapter for download")
    argparser.add_argument("--info-only", dest="info_only", action="store_true", 
        help="Shows only info about manga, not downloading")
    argparser.add_argument("--pdf", dest="pdf", action="store_true", 
        help="Converts the manga to a `.pdf` file after downloading. (Converts each volume into a new file)")
    argparser.add_argument("--pdf-only", dest="pdf_only", action="store_true", 
        help="Converts the manga to `.pdf` without downloading")
    argparser.add_argument("--vol-start", dest="vstart", type=int, 
        help="The number of the first volume for converting")
    argparser.add_argument("--vol-end", dest="vend", type=int, 
        help="The number of the last volume for converting")
    args = argparser.parse_args()

    if (args.start and args.end) and (args.start > args.end):
        error("-s cannot be more then -e")
        sys.exit(1)
    if args.start == 0:
        print("The volume with number 0 doesn't exists!")

    trace("Searching {}...".format(args.url))
    manga = parser.Manga(args.url)  

    DEFAULT_START = args.start or 1
    DEFAULT_END = args.end or manga.ch_count
    DEFAULT_VSTART = args.vstart or 1
    DEFAULT_VEND = args.vend or manga.vol_count
    PDF_FILE_NAME = "{0}/{0} том {1}.pdf"
    trace("Found!")

    print("\n\nAbout:")
    info(f"Title: {manga.name}")
    info(f"Chapters: {manga.ch_count}")
    info(f"Volumes: {manga.vol_count}\n")

    if args.info_only:
        print("Volumes:")
        for vol_num, ch_nums in manga.volumes.items():
            if len(ch_nums) <= 1:
                info(f"{vol_num}: only {ch_nums[0]} chapter.")
                continue
            info(f"{vol_num}: {ch_nums[0]}-{ch_nums[-1]} chapter.")                
        return

    if not args.pdf_only:
        trace(f"Downloading from {DEFAULT_START} ch to {DEFAULT_END} ch")
        manga.download(DEFAULT_START, DEFAULT_END, f"./{manga.name}")

    if args.pdf or args.pdf_only:
        trace("Converting...")
        
        for vol_num in range(DEFAULT_VSTART, DEFAULT_VEND + 1):
            create_pdf(manga, manga.name, PDF_FILE_NAME.format(manga.name, vol_num), vol_num)

if __name__ == '__main__':
    main()
