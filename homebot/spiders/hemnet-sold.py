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

from ..items import AdvertisementItem

from scrapy import Spider, Request

from datetime import datetime

import re
import json

DEFAULT_URL = "https://www.hemnet.se/salda/bostader"

class HemnetSoldSpider(Spider):
    name = "hemnet-sold"
    allowed_domains = ["www.hemnet.se"]

    def start_requests(self):
        url = getattr(self, "url", DEFAULT_URL)
        yield Request(url, self.parse)

    def parse(self, response):
        ads = response.xpath("//ul[@id='search-results']/li/div/a/@href")
        for url in ads.extract():
            yield Request(url, self.parse_advertisement)

        next_page = response.xpath("//a[contains(@class, 'next_page')]/@href") \
                            .extract_first()
        if next_page is not None:
            yield Request(response.urljoin(next_page))

    def parse_advertisement(self, response):
        item = AdvertisementItem()

        item["url"] = response.url

        s = "normalize-space(//p[@class='sold-property__metadata']/text()[2])"
        metadata = response.xpath(s).extract_first()
        metadata = re.split(" - ", metadata)
        item["object_type"] = metadata[0]
        item["region"] = metadata[1]

        s = "//p[@class='sold-property__metadata']/time/@datetime"
        item["sold_date"] = response.xpath(s).extract_first()

        item["rent"]  = self._get_attrib_from_html(response, "Avgift/månad")
        item["fee"] = self._get_attrib_from_html(response, "Driftskostnad")

        year = self._get_attrib_from_html(response, "Byggår")
        try:
            # If multiple years, only extract the initial
            year = re.search("^[\d]{4}", year).group()
        except Exception:
            year = 0
        item["construction_year"] = year

        item["housing_association"] = self._get_attrib_from_html(response,
                                                                 "Förening")

        s = "//div[@class='broker__details']/p[2]//text()[1]"
        try:
            firm = response.xpath(s).extract()[0].strip()
            if firm == "":
                firm = response.xpath(s).extract()[1].strip()
        except IndexError:
            firm = ""
        item["broker_firm"] = firm

        s = "//script[@type='text/javascript'][3]/text()"
        script = response.xpath(s).extract_first()
        attribs = re.search("var properties = \[(.*)]\;", script).group(1)
        try:
            attribs = json.loads(attribs)

            item["address"] = attribs["address"]
            item["latitude"] = attribs["coordinate"][0]
            item["longitude"] = attribs["coordinate"][1]

            item["object_type"] = attribs["type"]

            item["rooms"] = attribs["rooms"]

            item["living_area"] = attribs["living_space"]
            item["lot_area"] = attribs["land_area"]
            item["gross_area"] = attribs["supplemental_area"]

            item["list_price"] = attribs["asked_price"]
            item["sold_price"] = attribs["price"]
        except json.JSONDecodeError:
            # Some adds doesn't have the properties in JavaScript, extract as
            # much as possible from HTML instead
            self.parse_attribs_from_html(response, item)

        item["last_updated"] = datetime.now()

        self._strip_attribs(item)

        yield item

    def parse_attribs_from_html(self, response, item):
        s = "normalize-space(//h1[@class='sold-property__address']/text()[2])"
        item["address"] = response.xpath(s).extract_first()

        s = "//span[@class='sold-property__price-value']/text()"
        item["sold_price"] = response.xpath(s).extract_first()

        s = "//dl[@class='sold-property__price-stats']/dd[2]/text()"
        item["list_price"] = response.xpath(s).extract_first()

        item["rooms"] = self._get_attrib_from_html(response, "Antal rum")

        item["living_area"] = self._get_attrib_from_html(response, "Boarea")
        item["lot_area"] = self._get_attrib_from_html(response, "Tomtarea")
        item["gross_area"] = self._get_attrib_from_html(response, "Biarea")

        # This attribute was parsed from HTML earlier, but since we had to parse
        # everything else from HTML as well we need to normalize it to be
        # consistent with the JavaScript properties.
        item["object_type"] = self._normalize_object_type(item["object_type"])

    def _get_attrib_from_html(self, response, attrib):
        s = "//dl[@class='sold-property__attributes']"
        attribs = response.xpath(s)
        s = "normalize-space(//dt[text()='{}']/following-sibling::dd/text())"
        return attribs.xpath(s.format(attrib)).extract_first()

    def _normalize_object_type(self, s):
        if "bostadsrätt" in s.lower():
            return "bostadsratt"
        elif "fritidshus" in s.lower():
            return "fritidshus"
        elif "villa" in s.lower():
            return "villa"
        elif "rad" in s.lower():
            return "radhus"
        else:
            return s

    def _strip_attribs(self, item):
        keys = ("latitude", "longitude", "rooms", "living_area", "lot_area",
                "gross_area")
        for key in keys:
            item[key] = self._strip_to_float(item.get(key, 0.0))

        keys = ("construction_year", "rent", "fee", "list_price", "sold_price")
        for key in keys:
            item[key] = self._strip_to_int(item.get(key, 0))

    def _strip_to_float(self, n):
        # There's probably a more Pythonic way of doing this...
        if type(n) is str:
            try:
                return float(re.sub("[^0-9,\.]", "", n).replace(",", "."))
            except Exception:
                return 0.0

        if n is None:
            return 0.0

        return float(n)

    def _strip_to_int(self, n):
        return int(self._strip_to_float(n))
