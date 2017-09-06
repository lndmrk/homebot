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

from scrapy import Item, Field

class HemnetSoldItem(Item):
    url = Field(serializer=str)

    address = Field(serializer=str)
    region = Field(serializer=str)
    latitude = Field(serializer=float)
    longitude = Field(serializer=float)

    object_type = Field(serializer=str)
    construction_year = Field(serializer=int)

    rooms = Field(serializer=float)

    living_area = Field(serializer=float)
    lot_area = Field(serializer=float)
    gross_area = Field(serializer=float)

    rent = Field(serializer=int)
    yearly_fee = Field(serializer=int)

    list_price = Field(serializer=int)
    sold_price = Field(serializer=int)

    sold_date = Field(serializer=str)

    housing_association = Field(serializer=str)

    broker_firm = Field(serializer=str)

    last_updated = Field(serializer=str)
