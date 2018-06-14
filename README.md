# Get to know the FIFA world cups :tada:

In order to better place my bets for the world cup games 2018, I want to look at how the games typically ended in previous world cups to complement the knowledge of bookie odds with past game stats.

To gather the past FIFA world cup data, I'll scrape wikipedia using [scrapy](https://scrapy.org).

Install scrapy:

```
pip install scrapy
```

Generate the data files with past world cup data:

```
scrapy crawl worldcup2014 -o data/worldcup2014.json
```
