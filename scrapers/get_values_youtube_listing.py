import json
from pprint import pprint
from datetime import timedelta
from difflib import SequenceMatcher
from youtube_search import YoutubeSearch


def _get_similar_strings(a:str, b:str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def _produce_duration_parse(duration:str) -> int:
    value_splited = duration.split(':')[::-1]
    return sum(
        int(i)*j for i, j in 
        zip(
            value_splited,
            (1, 60, 3600),
        )
    )

def _produce_duration_inverse(duration_inverse:int) -> int:
    return str(timedelta(seconds=duration_inverse))

def get_links_filtered(
    value_result:list,
    value_name:str,
    value_duration:int
) -> dict:
    value_return = []
    live = 'Live'.lower()
    for element in (
        i for i in value_result 
        if abs(value_duration - i.get("duration")) <= 3 and
        (
            all(live in i.lower() for i in [value_name, i.get("title")]) or
            all(not live in i.lower() for i in [value_name, i.get("title")])
        )  
    ):
        element.update(
            {
                "sequence": _get_similar_strings(
                    _replace_unneccessary_input(value_name),
                    element.get("title")
                ),
                "name_searched": value_name,
                "accurate": True,
                
            }
        )
        value_return.append(element)
    return sorted(
        value_return,
        key=lambda x: x["sequence"],
        reverse=True,
    )[0] if value_return else {
        **{
            "sequence": _get_similar_strings(
                _replace_unneccessary_input(value_name),
                    value_result[0].get("title")
                ),
                "accurate": False,
        },
        **value_result[0]
    }

def _replace_unneccessary_input(title:str) -> str:
    for i, j in [
        [" / ", "/"],
        ["\xa0", ""]
    ]:
        title = title.replace(i, j)
    return title

def _replace_unneccessary_title(title:str) -> str:
    for i in [
        "(Official Video)",
        "(Official Audio)",
        "(Official Music Video)",
        "(Audio)",
        "(Visualizer)",
        "[Official Video]",
        "[Official Audio]",
        "[Official Music Video]",
        "[Audio]",
        "[Visualizer]",
    ]:
        title = title.replace(i, '')
    return title.strip()

def get_links_search(value_string:str) -> list:
    results_parsed = []
    results = YoutubeSearch(
        _replace_unneccessary_input(value_string),
        max_results=4
    )
    results = results.to_json()
    for element in json.loads(results).get('videos', []):
        # print(element)
        # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        if (duration:=element.get("duration")) and len(duration.split(':')) > 3:
            continue
        results_parsed.append(
            {
                "url": f"https://www.youtube.com/watch?v={element.get('id')}",
                "duration": _produce_duration_parse(duration),
                "title": _replace_unneccessary_title(element.get("title")),
                # "views": int(
                #     element.get("views", '').replace('\xa0', '').strip().split(' ')[0]
                # )
            }
        )
    return results_parsed
    # return sorted(
    #     results_parsed,
    #     key=lambda x: x.get("views", -1),
    #     reverse=True
    # )


if __name__ == "__main__":
    # results = get_links_search("asap rocky peso")
    # pprint(results)
    a = get_links_search('Run The Jewels - Down (feat. Joi)')
    pprint(a)
    print('#########################################')
    print(get_links_filtered(a, 'Run The Jewels - Down (feat. Joi)', 192))
# print(results.keys())