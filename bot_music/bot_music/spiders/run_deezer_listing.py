from scrapy import Spider, Request


class DeezerListing(Spider):
    """
    
    """
    def __init__(self, name=None, **kwargs):
        self._urls = [] #TODO change it later

    def start_requests(self):
        for url in self._urls:
            yield Request(
                url=url,
                method='GET',
                callback=self.parse,
                headers=None, #TODO add later,
                cb_kwargs=None, #TODO add later
            )

    def parse(self, response):
        print(response.status)
        