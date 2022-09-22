from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from bot_music.spiders.run_youtube_listing import collect_youtube_search

@defer.inlineCallbacks
def run_scraping(
    runner: CrawlerRunner,
):
    #TODO change that after
    yield runner.crawl(
        'deezer_listing',
        name = 'search_song',
        searches = [
            'bones',
        ]
    )

    reactor.stop()
    

def main():
    configure_logging()
    try:
        run_scraping(
            runner=CrawlerRunner(get_project_settings()),
        )
        reactor.run()

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()