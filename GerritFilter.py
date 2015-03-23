from __future__ import print_function, absolute_import, unicode_literals

from afew.filters.BaseFilter import Filter
from afew.FilterRegistry import register_filter


@register_filter
class GerritFilter(Filter):
    message = 'Tagging Gerrit messages'

    simple_headers = [
        'x-gerrit-messagetype',
    ]

    def handle_message(self, message):
        if message.get_header('x-gerrit-messagetype'):
            self.add_tags(message, 'bug', 'bug/gerrit')

            for header in self.simple_headers:
                data = message.get_header(header)
                if not data:
                    continue

                data = data.replace(' ', '-')
                data = data.lower()

                header = header[9:]
                self.add_tags(message, 'gerrit/{}/{}'.format(header, data))
