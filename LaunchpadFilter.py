from __future__ import print_function, absolute_import, unicode_literals

import re

from afew.filters.BaseFilter import Filter
from afew.FilterRegistry import register_filter


@register_filter
class LaunchpadFilter(Filter):
    message = 'Tagging Launchpad messages'

    simple_headers = [
        'x-launchpad-bug-tags',
        'x-launchpad-bug-information-type',
        'x-launchpad-bug-private',
        'x-launchpad-bug-security-vulnerability',
    ]

    def handle_message(self, message):
        if message.get_header('x-launchpad-bug'):
            self.add_tags(message, 'bug')

            match = re.search('\[Bug (?P<bugid>\d+)\]',
                              message.get_header('subject'))
            if match:
                self.add_tags(message, 'bug/{}'.format(match.group(1)))

            for header in self.simple_headers:
                data = message.get_header(header)
                if not data:
                    continue

                data = data.replace(' ', '-')
                data = data.lower()

                header = header[16:]
                for value in data.split():
                    self.add_tags(message, 'lp/{}/{}'.format(header, value))

