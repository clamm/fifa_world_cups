# -*- coding: utf-8 -*-
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


    def parse(self, response):
        common_path = '//div[@itemscope="itemscope"]/table/tr[@itemprop="name"]/'
        home_teams = response.xpath(common_path + 'th[@itemprop="homeTeam"]/span/a/text()').extract()
        away_teams = response.xpath(common_path + 'th[@itemprop="awayTeam"]/span/span/a/text()').extract()
        scores_at_ninety_min = response.xpath(common_path + 'th/text()').extract()

        groups = response.xpath('//h3//span[contains(@id, "Group")]/text()').extract()
        games_per_group = 6
        # 8 groups à 6 games, 8 games in the game of 16, 4 games in quarter finals, 2 games in semi finals, 2 games in finals
        total_games = 8 * 6 + 8 + 4 + 2 + 2

        for total_games_idx in range(total_games):
            group_index = total_games_idx // 6
            yield {
                'total_game_index': total_games_idx,
                'game_number_within_game_type': self.game_number(total_games_idx),
                'game_type': self.game_type(total_games_idx),
                'group': groups[group_index] if group_index < len(groups) else None,
                'home_team': home_teams[total_games_idx],
                'away_team': away_teams[total_games_idx],
                'score_at_90_min': scores_at_ninety_min[total_games_idx]
            }
