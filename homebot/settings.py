# Copyright (C) 2017 Emil Lundmark
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

BOT_NAME = "homebot"

SPIDER_MODULES = ["homebot.spiders"]

AUTOTHROTTLE_ENABLED = True

COOKIES_ENABLED = False

# Enable caching during development
HTTPCACHE_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "homebot.middlewares.RandomUserAgentMiddleware": 100,
}

# Requires a Google Maps API key in environment variable GOOGLE_API_KEY
#from datetime import datetime
#ITEM_PIPELINES = {
#    "homebot.pipelines.TravelTimePipeline": 100,
#}
#TRAVEL_DESTINATION = ""
#TRAVEL_ARRIVAL_TIME = datetime(2017, 9, 17, 21, 0)
#TRAVEL_MAX_TRAVEL_TIME = 30 * 60

#SPIDER_MIDDLEWARES = {
#    "scrapy_deltafetch.DeltaFetch": 100,
#}
#DELTAFETCH_ENABLED = True
