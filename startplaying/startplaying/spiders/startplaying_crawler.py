import json
import re

import jmespath
import scrapy
from startplaying.items import StartplayingItem
from startplaying.spiders.template import payload_template


class StartplayingCrawlerSpider(scrapy.Spider):
    name = "startplaying_crawler"
    allowed_domains = ["startplaying.com"]

    def start_requests(self):
        qraph_ql_url = 'https://startplaying.games/api/graphql'
        payload = payload_template.copy()
        yield scrapy.Request(
            qraph_ql_url,
            method='POST',
            body=json.dumps(payload),
            callback=self.parse
        )

    def parse(self, response):
        data = response.json()
        games = jmespath.search('data.sessions.edges[].node', data)

        for game in games or []:
            grid_data = self._parse_grid_data(game)
            game_request = self._create_game_request(grid_data)
            yield game_request

        has_next_page = jmespath.search('data.sessions.pageInfo.hasNextPage', data)
        if has_next_page:
            next_page_request = self._create_next_page_request(data)
            yield next_page_request

    def _create_next_page_request(self, data: dict) -> scrapy.Request:
        cursor = jmespath.search('data.sessions.pageInfo.endCursor', data)
        payload = payload_template.copy()
        payload['variables']['after'] = cursor
        return scrapy.Request(
            method='POST',
            dont_filter=True,
            url='https://startplaying.games/api/graphql',
            body=json.dumps(payload),
            callback=self.parse
        )

    def _create_game_request(self, grid_data: dict) -> scrapy.Request:
        url = grid_data.get('url')
        return scrapy.Request(
            dont_filter=True,
            url=url,
            callback=self.parse_game,
            cb_kwargs={'grid_data': grid_data}
        )

    def parse_game(self, response, grid_data: dict):
        grid_data['tactical_level'] = self._parse_tactical_level(response)
        item = StartplayingItem(**grid_data)
        yield item

    def _parse_grid_data(self, game: dict) -> dict:
        return {
            'title': jmespath.search('adventure.title', game),
            'url': f"https://startplaying.games/adventure/{jmespath.search('adventure.slug', game)}",
            'cost': f"{jmespath.search('adventure.costPerPlayer', game)}$",
            'image': jmespath.search('gameTemplate.coverImage', game),
            'game_system': jmespath.search('gameTemplate.gameSystems[0].name', game),
            'seats_left': self._calculate_seats(game)
        }

    def _parse_tactical_level(self, response) -> str:
        pattern = 'Combat/Tactics: (.*?)<'
        found = re.search(pattern, response.text)
        if found:
            return found.group(1)

    def _calculate_seats(self, game: dict) -> int | None:
        max_players = jmespath.search('adventure.maxPlayers', game)
        current_players = jmespath.search('numPlayers', game)
        return int(max_players) - int(current_players) if max_players and current_players else None
