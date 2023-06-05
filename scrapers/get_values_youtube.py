import os
import shutil
import traceback
import yt_dlp as youtube_dl
from uuid import uuid4
from pprint import pprint
from urllib.parse import (
    urlparse,
    parse_qs,    
)
from pytube import (
    YouTube,
    Playlist,
    exceptions,
)
from config import (
    PATH_USE,
    PATH_STORAGE,
    MAX_RETRY_COUNT,
)

def get_selector_use(url:str) -> bool:
    parsed_string_dict = parse_qs(urlparse(url).query)
    return str(parsed_string_dict['v']).replace("'", '')

def check_link_playlist(url:str) -> bool:
    parsed_string_dict = parse_qs(urlparse(url).query)
    return 'list' in parsed_string_dict.keys()

def get_new_name() -> str:
    return f"{uuid4()}.mp3"

def produce_additional_download(
    link_youtube:str, 
    original_sender:str = 'test',
    id:int = None,
    max_retries:int = 0
) -> dict[str|list]:
    if max_retries > MAX_RETRY_COUNT:
        return {
            get_new_name(): {
                "sender": original_sender,
                "title": '',
                "id": id,
                "success": False,
            }
        }
    value_result = {}
    ydl_opts = {
        'format': 'bestaudio/best',
        'nocheckcertificate': True, #TODO check it later
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }
        ]
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(
                [
                    link_youtube,
                ]
            )
        selector_check = get_selector_use(link_youtube)
        for filename in os.listdir(PATH_USE):
            if not selector_check in filename:
                continue
            shutil.move(
                os.path.join(PATH_USE, filename),
                os.path.join(PATH_STORAGE, (new_name:=get_new_name()))
            )
            value_result[new_name] = {
                "sender": original_sender,
                "title": filename.split(selector_check)[0].strip(),
                "id": id, 
                "success": True
            }
        return value_result
    except Exception:
        print(error:=traceback.format_exc())
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        return produce_additional_download(
            link_youtube,
            original_sender,
            id,
            max_retries + 1
        )

def produce_file_download_internet(
        link_youtube:str, 
        original_sender:str = 'test',
        id:int = None,
        max_retries:int = 0

) -> dict[str|list]:
    value_dct = {}
    if max_retries > MAX_RETRY_COUNT:
        yt = YouTube(
            link_youtube, 
            allow_oauth_cache=False,
        )
        return {
            get_new_name(): {
                "sender": original_sender,
                "title": yt.title,
                "id": id,
                "success": False,
            }
        }
    if not check_link_playlist(link_youtube):
        urls = [
            [0 if id is None else id, link_youtube]
        ]
    else:
        urls = enumerate(Playlist(link_youtube).video_urls)
    for id, url in urls:
        try:
            yt = YouTube(
                url, 
                allow_oauth_cache=False,
            )
            if yt.check_availability():
                value_dct.update(
                    {
                        get_new_name(): {
                            "sender": original_sender,
                            "title": yt.title,
                            "id": id,
                            "success": False,
                        }
                    }
                )
                continue
            stream = sorted(
                yt.streams.filter(only_audio=True),
                key=lambda x: int(x.abr.replace('kbps', '')),
            )[-1]
            #stream = yt.streams.filter(only_audio=True,).first()
            stream.download(
                PATH_STORAGE,
                new_name:=get_new_name(),
                skip_existing=True,
                max_retries=MAX_RETRY_COUNT
            )
            value_dct.update(
                {
                    new_name:  {
                        "sender": original_sender,
                        "title": yt.title,
                        "id": id,
                        "success": True,
                    }
                }
            )
        except exceptions.AgeRestrictedError:
            value_dct.update(
                produce_additional_download(
                    url,
                    original_sender,
                    id,
                    max_retries
                )
            )
    return value_dct


if __name__ == "__main__":
    a = produce_file_download_internet(
        # 'https://www.youtube.com/watch?v=Hll8zxAbvH0'
        # "https://www.youtube.com/watch?v=4C-H7Mr7hGg&list=PLRW80bBvVD3XsSk0eXKIQW_kZMMsQtlz-&index=19&ab_channel=SonySoundtracksVEVO",
        'https://www.youtube.com/watch?v=dsnuu20RSFU&ab_channel=MetroBoominVEVO',
    )


