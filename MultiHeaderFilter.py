from __future__ import print_function, absolute_import, unicode_literals

import re

from afew.filters.BaseFilter import Filter
from afew.FilterRegistry import register_filter

@register_filter
class MultiHeaderFilter(Filter):
    message = 'Tag message containing pattern in one of many headers'
    headers = []
    tags = []
    pattern = None

    def handle_message(self, message):
        if not self.pattern:
            self.log.warn('no pattern defined (skipping)')
            return

        for header in self.headers:
            value = message.get_header(header)
            if re.search(self.pattern, value):
                self.add_tags(message, *self.tags)

