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

import googlemaps
import os

from datetime import datetime

from scrapy.exceptions import DropItem

class TravelTimePipeline(object):
    def __init__(self, destination, arrival_time, max_travel_time):
        self._destination = destination
        self._max_travel_time = max_travel_time
        self._arrival_time = arrival_time
        key = os.environ["GOOGLE_API_KEY"];
        self._gmaps = googlemaps.Client(key=key)

    def process_item(self, item, spider):
        latitude = item.get("latitude")
        longitude = item.get("longitude")
        travel_time = -1

        if latitude and longitude:
            result = self._gmaps.distance_matrix(
                origins=(latitude, longitude),
                destinations=self._destination,
                mode="transit",
                arrival_time=self._arrival_time)
            travel_time = result["rows"][0]["elements"][0]["duration"]["value"]
            if travel_time > self._max_travel_time:
                raise DropItem("Travel time {} too long".format(travel_time))

        item["travel_time"] = travel_time

        return item

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get("TRAVEL_DESTINATION"),
                   settings.get("TRAVEL_ARRIVAL_TIME"),
                   settings.getint("TRAVEL_MAX_TRAVEL_TIME"))
