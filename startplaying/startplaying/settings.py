BOT_NAME = "startplaying"

SPIDER_MODULES = ["startplaying.spiders"]
NEWSPIDER_MODULE = "startplaying.spiders"

ROBOTSTXT_OBEY = False
CLOSESPIDER_ITEMCOUNT = 1000
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/124.0.0.0 Safari/537.36'
DEFAULT_REQUEST_HEADERS = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,uk;q=0.8,ru;q=0.7,it;q=0.6,pt;q=0.5',
            'content-type': 'application/json',
            'origin': 'https://startplaying.games',
            'priority': 'u=1, i',
            'referer': 'https://startplaying.games/search',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
FEEDS = {
    'items.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'indent': 4,
        'overwrite': True,
    },
}