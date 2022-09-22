from youtube_search import YoutubeSearch


def collect_youtube_search(search_item:str) -> dict:
    return YoutubeSearch(
        search_item, 
        max_results=10
    ).to_json()
