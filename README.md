# HomeBot
A tool for obtaining and analyzing data from the Swedish housing market.

## Install
The following should get you started on most systems.
```
$ pip3 install -r requirements.txt
```

## Obtaining data
Data is obtained using *spiders* with [Scrapy]. Run
```
$ scrapy --help
```
for general help with Scrapy. To fetch data you need to get a spider *crawling*.
```
$ scrapy crawl [options] <spider>
```
You can pass `-a url=<url>` to change the starting URL for your crawls. See
```
$ scrapy list
```
for a list of available spiders.

Also see [settings.py] for some options that could be useful!

### Example
Fetch all items from [Hemnet] with at least 10 rooms to a JSON file.
```
$ scrapy crawl \
         -a url="https://www.hemnet.se/salda/bostader?rooms_min=10.0" \
         --output-format=json \
         --output=homebot.json \
         hemnet-sold
```

## Analyzing data
When you got some data, it's time to analyze!

### SQL
SQL is a nice language for relational databases. Even though we don't really
have any relational data, it's still useful for doing aggregation and filtering.

You can use [sqlitebiter] to convert e.g. a JSON file to a [SQLite] format. 
```
$ sqlitebiter file homebot.json --output-path=homebot.sql
$ sqlite3 homebot.sql
sqlite> SELECT AVG(soldprice) FROM homebot_json1;
6047405.62248996
```

## Inspiration
This project was inspired by Lauri Vanhala's article
[Figuring out the best place to live in Helsinki].


[Hemnet]: https://www.hemnet.se/
[Scrapy]: https://scrapy.org/
[settings.py]: homebot/settings.py
[sqlitebiter]: https://sqlitebiter.readthedocs.io/
[SQLite]: https://www.sqlite.org/
[Figuring out the best place to live in Helsinki]: http://www.wanhala.net/post/156484186523/figuring-out-the-best-place-to-live-in-helsinki
