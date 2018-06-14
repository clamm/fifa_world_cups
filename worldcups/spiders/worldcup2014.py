# -*- coding: utf-8 -*-
import scrapy

class Worldcup2014Spider(scrapy.Spider):
    name = 'worldcup2014'
    start_urls = ['https://en.wikipedia.org/wiki/2014_FIFA_World_Cup']

    def parse(self, response):
        home_teams = response.xpath('//div[@itemscope="itemscope"]/table/tr[@itemprop="name"]/th/span/a/text()').extract()

        for index, group in enumerate(response.xpath('//h3//span[contains(@id, "Group")]/text()').extract()):


            yield {
                'index': index,
                'group': group,
                'home_team': home_teams[index]
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
