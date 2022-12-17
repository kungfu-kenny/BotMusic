from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from bot_music.spiders.run_youtube_listing import collect_youtube_search


@defer.inlineCallbacks
def run_scraping(
    runner: CrawlerRunner,
    name:str,
    searches:list,
    listing_name:str='deezer_listing',
):
    #TODO change that after
    #TODO work on the argparse values
    yield from runner.crawl(
        listing_name,
        name=name,
        searches=searches,
    )

    reactor.stop()
    

def main_configuration(name:str='search_song', searches:list=['bones']):
    configure_logging()
    try:
        k = run_scraping(
            runner=CrawlerRunner(get_project_settings()),
            listing_name='deezer_listing',
            searches=searches,
            name=name,
        )
        reactor.run()
        print(k)
        print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main_configuration()