# Copyright (C) 2017 Emil Lundmark
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU # General Public License as published by the Free
# Software Foundation, version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

BOT_NAME = "homebot"

SPIDER_MODULES = ["homebot.spiders"]

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "homebot.middlewares.RandomUserAgentMiddleware": 100,
}

AUTOTHROTTLE_ENABLED = True

# Enable caching during development
HTTPCACHE_ENABLED = False

# Enable incremental fetches (requires extra dependencies)
#SPIDER_MIDDLEWARES = {
#    "scrapy_deltafetch.DeltaFetch": 100,
#}
#DELTAFETCH_ENABLED = True
