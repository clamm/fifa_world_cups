# Get to know the FIFA world cups :tada:

In order to better place my bets for the world cup games 2018, I want to look at how the games typically ended in previous world cups to complement the knowledge of bookie odds with past game stats.

To gather the past FIFA world cup data, I'll scrape wikipedia using [scrapy](https://scrapy.org).

Install scrapy:

```
pip install scrapy
```

Generate the data json file with past world cup data:

```
cd data_acquisition
scrapy crawl worldcup2014 -o data/worldcup2014.json
```

Analyse data with [jupyter](http://jupyter.org), run the following to start the jupyter server locally:

```
jupyter notebook
```

Notebook: [fifa_world_cups](./data_analysis/fifa_world_cups.ipynb)
