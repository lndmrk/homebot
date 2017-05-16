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

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from fake_useragent import UserAgent

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent):
        self.fake_ua = UserAgent()
        super(RandomUserAgentMiddleware, self).__init__(user_agent)

    def process_request(self, request, spider):
        request.headers.setdefault(b"User-Agent", self.fake_ua.random)
