from __future__ import print_function, absolute_import, unicode_literals

import re

from afew.filters.BaseFilter import Filter
from afew.FilterRegistry import register_filter


@register_filter
class BugzillaFilter(Filter):
    message = 'Tagging Bugzilla messages'
    pattern = '\[Bug (?P<bugid>\d+)\]'

    headers = [
        ('x-bugzilla-reason'         , True , None) ,
        ('x-bugzilla-type'           , False , None) ,
        ('x-bugzilla-watch-reason'   , False , None) ,
        ('x-bugzilla-classification' , False , None) ,
        ('x-bugzilla-product'        , False , None) ,
        ('x-bugzilla-component'      , False , None) ,
        ('x-bugzilla-severity'       , False , None) ,
        ('x-bugzilla-status'         , False , None) ,
        ('x-bugzilla-priority'       , False , None) ,
        ('x-bugzilla-flags'          , True  , ', ') ,
    ]

    def handle_message(self, message):
        if message.get_header('x-bugzilla-url'):
            self.add_tags(message, 'bug', 'bug/bz')

            match = re.search(self.pattern,
                              message.get_header('subject'))
            if match:
                self.add_tags(message,
                              'bug/{bugid}'.format(**match.groupdict()))

            for header, needs_split, sep in self.headers:
                data = message.get_header(header)
                if not data:
                    continue

                data = data.lower()

                if needs_split:
                    data = data.split(sep)
                else:
                    data = [data.replace(' ', '-')]

                header = header[11:]
                for val in data:
                    self.add_tags(message, 'bz/{}/{}'.format(header, val))
