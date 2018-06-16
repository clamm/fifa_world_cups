# -*- coding: utf-8 -*-
import re
import scrapy

class Worldcup2014Spider(scrapy.Spider):
    name = 'worldcup2014'
    start_urls = ['https://en.wikipedia.org/wiki/2014_FIFA_World_Cup']

    def game_type(self, total_games_idx):
        if total_games_idx < 48:
            return "group"
        elif total_games_idx < 56:
            return "round of 16"
        elif total_games_idx < 60:
            return "quarter final"
        elif total_games_idx < 62:
            return "semi final"
        elif total_games_idx < 63:
            return "third place play-off"
        elif total_games_idx == 63:
            return "final"
        else:
            raise Exception("game type unknown")

    def game_number(self, total_games_idx):
        game_type = self.game_type(total_games_idx)
        nb_group_games = 8 * 6
        nb_round_16_games = 8
        nb_quarter_finals = 4

        if game_type == "group":
            group_index = total_games_idx // 6
            return total_games_idx + 1 - group_index * 6
        elif game_type == "round of 16":
            return total_games_idx + 1 - nb_group_games
        elif game_type == "quarter final":
            return total_games_idx + 1 - nb_group_games - nb_round_16_games
        elif game_type == "semi final":
            return total_games_idx + 1 - nb_group_games - nb_round_16_games - nb_quarter_finals
        else:
            return 1

    def group(self, groups, total_games_idx):
        group_index = total_games_idx // 6
        return groups[group_index] if group_index < len(groups) else None

    def clean_score(self, score_string):
        # we don't match a dash between the number groups as the scraped dash seems to be different (longer) than the typed dash
        return re.sub(r'(\d{1,2}).(\d{1,2})(.*)', r'\1-\2', score_string)

    def parse(self, response):
        common_path = '//div[@itemscope="itemscope" and not(@itemprop)]'
        teams_and_scores = 'table/tr[@itemprop="name"]'
        rel = './'

        groups = response.xpath('//h3//span[contains(@id, "Group")]/text()').extract()

        for total_games_idx, game in enumerate(response.xpath(common_path)):
            # each div contains a div (times), table (scores) and another div (location, referee)
            home_team = game.xpath(rel + teams_and_scores + '/th[@itemprop="homeTeam"]/span/a/text()').extract_first()
            away_team = game.xpath(rel + teams_and_scores + '/th[@itemprop="awayTeam"]/span/span/a/text()').extract_first()
            score = game.xpath(rel + teams_and_scores + '/th/text()').extract_first()

            yield {
                'total_game_index': total_games_idx,
                'game_number_within_game_type': self.game_number(total_games_idx),
                'game_type': self.game_type(total_games_idx),
                'group': self.group(groups, total_games_idx),
                'home_team': home_team,
                'away_team': away_team,
                'score': self.clean_score(score)

            }
