import os
import pandas as pd


albums = []
artists = []

def return_start_links(search_type:str, link_type:str) -> list:
    return {
        "deezer": return_start_link_deezer,
        None: return_none,
    }.get(search_type, None)(link_type)

def return_none(_='') -> list:
    return []

def return_start_link_deezer(link_type:str, search:str='') -> list:
    if link_type == 'album':
        return [
            f'https://www.deezer.com/search/{i}/album'
            for i in albums
        ]
    elif link_type == 'artist':
        return [
            f'https://www.deezer.com/search/{i}/artist'
            for i in artists
        ]
    elif link_type == 'all':
        return [
            f'https://www.deezer.com/search/{search}/artist'
        ]
    return []