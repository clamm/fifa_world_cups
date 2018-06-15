# -*- coding: utf-8 -*-
import scrapy

class Worldcup2014Spider(scrapy.Spider):
    name = 'worldcup2014'
    start_urls = ['https://en.wikipedia.org/wiki/2014_FIFA_World_Cup']

    def parse(self, response):
        common_path = '//div[@itemscope="itemscope"]/table/tr[@itemprop="name"]/'
        home_teams = response.xpath(common_path + 'th[@itemprop="homeTeam"]/span/a/text()').extract()
        away_teams = response.xpath(common_path + 'th[@itemprop="awayTeam"]/span/span/a/text()').extract()
        scores_at_ninety_min = response.xpath(common_path + 'th/text()').extract()

        games_per_group = 6
        for group_index, group in enumerate(response.xpath('//h3//span[contains(@id, "Group")]/text()').extract()):
            for game_index in range(group_index * games_per_group, group_index * games_per_group + games_per_group):
                yield {
                    # 'game_index': game_index,
                    'game': game_index + 1 - group_index * 6,
                    'group': group,
                    'home_team': home_teams[game_index],
                    'away_team': away_teams[game_index],
                    'score_at_90_min': scores_at_ninety_min[game_index]
                }


        # for quote in response.css('div.quote'):
        #     yield {
        #         'text': quote.css('span.text::text').extract_first(),
        #         'author': quote.xpath('span/small/text()').extract_first(),
        #     }
        #
        # next_page = response.css('li.next a::attr("href")').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
