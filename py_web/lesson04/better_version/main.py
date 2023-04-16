from pathlib import Path
from shutil import unpack_archive, ReadError
from concurrent.futures import ThreadPoolExecutor
from time import time
from typing import Dict, Tuple, List
from register_extensions import REGISTER_EXTENSIONS
from normalize import normalize_name
import logging


def sorter(folder) -> Dict[Tuple[str, str], List[Path]]:
    """
    Sorts files into folders by folder. Turns the dictionary
    """
    file_list = sorted(folder.glob("**/*"))
    result = {}
    for file in [files for files in file_list if files.is_file()]:
        ext = file.suffix[1:].upper()
        file_type = REGISTER_EXTENSIONS.get(ext, "other")
        if result.get((ext, file_type)):
            result[(ext, file_type)].append(file)
        else:
            result[(ext, file_type)] = [file]
    # for k, v in result.items():
    #     logging.debug(f"{k}: {v}")
    return result


def get_bad_folders(folder: Path) -> List[Path]:
    """
    Get bad folders
    """
    folder_list = [
        folder
        for folder in folder.glob("*")
        if folder.is_dir() and folder.name not in set(REGISTER_EXTENSIONS.values())
    ]

    bad_folders_list = [list(folder.glob("**/*")) for folder in folder_list]
    for lst in bad_folders_list:
        if lst:
            folder_list.extend(lst)

    return folder_list


def remove_folders(folders: List[Path]):
    """
    Deleting empty folders
    """
    positive_result = []
    negative_result = []
    for folder in folders[::-1]:
        try:
            folder.rmdir()
            positive_result.append(folder.name)
        except OSError:
            negative_result.append(folder.name)
    return positive_result, negative_result


def handle_archive(path) -> None:
    """
    Unpack archives to a new folder with the name of the archive and deletes it.
    """
    folder = path / "archives"
    list_for_archives_dirs = [dir_ for dir_ in folder.iterdir()]
    for target_folder in list_for_archives_dirs:
        list_for_archives_files = [path for path in target_folder.glob("**/*")]
        for archive in list_for_archives_files:
            # Create a folder for archives
            target_folder.mkdir(exist_ok=True, parents=True)
            #  Create a folder where we unpack the archive
            #  We take the suffix from the file and remove it replace(filename.suffix, '')
            folder_for_file = target_folder / normalize_name(archive.name.replace(archive.suffix, ''))
            #  Create a folder for the archive with the file name
            folder_for_file.mkdir(exist_ok=True, parents=True)
            try:
                # "zip", "tar", "gztar", "bztar", or "xztar"
                unpack_archive(str(archive.resolve()), str(folder_for_file.resolve()))
                logging.debug(f"Unpack archive: {folder_for_file.name}")
            except ReadError:
                logging.debug(f'The error is not an archive: {archive}!')
                folder_for_file.rmdir()
            archive.unlink()


def file_parser(*args):
    try:
        folder_for_scan = Path(args[0])
        sorted_file_dict = sorter(folder_for_scan.resolve())
    except FileNotFoundError:
        logging.debug(
            f"Not able to find '{args[0]}' folder. Please enter a correct folder name."
        )
    except IndexError:
        return "Please enter a folder name."
    except IsADirectoryError:
        logging.debug("Unknown file ")
    for file_types, files in sorted_file_dict.items():
        for file in files:
            if not (folder_for_scan / file_types[1]).exists():
                (folder_for_scan / file_types[1]).mkdir()
            if not (folder_for_scan / file_types[1] / file_types[0]).exists():
                (folder_for_scan / file_types[1] / file_types[0]).mkdir()
            file.replace(folder_for_scan / file_types[1] / file_types[0] / file.name)
    old_folder_list = get_bad_folders(folder_for_scan)
    positive, negative = remove_folders(old_folder_list)
    str_positive = "\n".join(positive)
    str_negative = "\n".join(negative)
    handle_archive(folder_for_scan)
    logging.debug(
        f"{'*' * 60}"
        "\n"
        f"Files in {args[0]} sorted successfully"
        "\n"
        f"Folders that are deleted: {str_positive}"
        "\n"
        f"Folders that are not deleted:{str_negative}"
        "\n"
        f"{'*' * 60}"
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    """ Speed better_version work with 1 Thread """
    # folder_for_scan = Path(input("Write the folder path >>> "))
    folder_for_scan = Path("E:\\Download\\sort1")
    timer = time()
    file_parser(folder_for_scan)
    print(f'Speed better_version work with 1 Thread {round(time() - timer, 4)}')
    """ Speed better_version work with Pool Threads = 2 """
    timer_1 = time()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(file_parser, Path("E:\\Download\\sort2"))
        logging.debug(f'Speed better_version work with Pool (2 Threads) = {round(time() - timer_1, 4)}')
    """ Speed better_version work with Pool Threads = 4 """
    timer_2 = time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(file_parser, Path("E:\\Download\\sort3"))
        logging.debug(f'Speed better_version work with Pool (4 Threads) = {round(time() - timer_2, 4)}')
