from __future__ import print_function, absolute_import, unicode_literals

import re

from afew.filters.BaseFilter import Filter
from afew.FilterRegistry import register_filter

@register_filter
class BugzillaFilter(Filter):
    message = 'Tagging Bugzilla messages'
    pattern = '\[Bug (?P<bugid>\d+)\]'

    simple_headers = [
            'x-bugzilla-reason',
            'x-bugzilla-type',
            'x-bugzilla-watch-reason',
            'x-bugzilla-classification',
            'x-bugzilla-product',
            'x-bugzilla-component',
            'x-bugzilla-severity',
            'x-bugzilla-status',
            'x-bugzilla-priority',
    ]

    def handle_message(self, message):
        if message.get_header('x-bugzilla-url'):
            self.add_tags(message, 'bug')

            match = re.search(self.pattern,
                              message.get_header('subject'))
            if match:
                self.add_tags(message,
                              'bug/{bugid}'.format(**match.groupdict()))

            for header in self.simple_headers:
                data = message.get_header(header)
                if not data:
                    continue

                data = data.replace(' ', '-')
                data = data.lower()

                header = header[11:]
                self.add_tags(message, 'bz/{}/{}'.format(header, data))

