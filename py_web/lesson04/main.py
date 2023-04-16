from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
from time import time
from file_parser import *
from normalize import normalize
import logging


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalize(filename.name)))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalize(filename.name)))


def handle_archive(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))

    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
    except shutil.ReadError:
        logging.debug(f'Wrong - it`s not an archive {filename}!')
        folder_for_file.rmdir()
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        logging.debug(f'Not able to delete {folder}')


def file_parser(*args):
    try:
        folder_for_scan = Path(args[0])
        scan(folder_for_scan.resolve())
    except FileNotFoundError:
        logging.debug(f"There isn`t '{args[0]}' folder. Try again.")
    except IndexError:
        logging.debug("Please enter a folder name you want to sort.")

    for file in JPEG_IMAGES:
        handle_media(file, Path(args[0]) / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, Path(args[0]) / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, Path(args[0]) / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, Path(args[0]) / 'images' / 'SVG')

    for file in AVI_VIDEO:
        handle_media(file, Path(args[0]) / 'video' / 'AVI')
    for file in MP4_VIDEO:
        handle_media(file, Path(args[0]) / 'video' / 'MP4')
    for file in MOV_VIDEO:
        handle_media(file, Path(args[0]) / 'video' / 'MOV')
    for file in MKV_VIDEO:
        handle_media(file, Path(args[0]) / 'video' / 'MKV')

    for file in DOC_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'DOC')
    for file in DOCX_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'DOCX')
    for file in TXT_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'TXT')
    for file in PDF_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'PDF')
    for file in XLSX_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'XLSX')
    for file in PPTX_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'PPTX')

    for file in MP3_AUDIO:
        handle_media(file, Path(args[0]) / 'audio' / 'MP3')
    for file in OGG_AUDIO:
        handle_media(file, Path(args[0]) / 'audio' / 'OGG')
    for file in WAV_AUDIO:
        handle_media(file, Path(args[0]) / 'audio' / 'WAV')
    for file in AMR_AUDIO:
        handle_media(file, Path(args[0]) / 'audio' / 'AMR')

    for file in ZIP_ARCHIVES:
        handle_archive(file, Path(args[0]) / 'archives')
    for file in GZ_ARCHIVES:
        handle_archive(file, Path(args[0]) / 'archives')
    for file in TAR_ARCHIVES:
        handle_archive(file, Path(args[0]) / 'archives')

    for file in OTHER:
        handle_other(file, Path(args[0]) / 'OTHER')

    for folder in FOLDERS[::-1]:
        handle_folder(folder)

    logging.debug(f'Files in {args[0]} was sorted.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    timer = time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(file_parser, Path("E:\\Download\\sort"))
        logging.debug(f'Speed test work with Pool (4 Threads) = {round(time() - timer, 4)}')
