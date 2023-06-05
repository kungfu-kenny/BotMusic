import os


def check_presence_folder(path_folder:str) -> None:
    (
        os.path.exists(path_folder) and os.path.isdir(path_folder)
    ) or os.mkdir(path_folder)

def check_presence_file(path_file:str, path_prev_check:bool=True) -> bool:
    return path_prev_check\
        and os.path.exists(path_file)\
        and os.path.isfile(path_file)

def download_music_telegram():
    pass