from __future__ import print_function, absolute_import, unicode_literals

from afew.filters.BaseFilter import Filter
from afew.FilterRegistry import register_filter


@register_filter
class RTFilter(Filter):
    message = 'Tagging RT messages'

    headers = [
            ('x-rt-queue'           , False , None) ,
            ('x-rt-priority'        , False , None) ,
    ]

    def handle_message(self, message):
        if message.get_header('x-rt-loop-prevention'):
            self.add_tags(message, 'req', 'req/rt')

            reqid = message.get_header('rt-ticket')
            if reqid:
                reqid = reqid.split()[1][1:]
                self.add_tags(message, 'req/{}'.format(reqid))

            for header, needs_split, sep in self.headers:
                data = message.get_header(header)
                if not data:
                    continue

                data = data.lower()

                if needs_split:
                    data = data.split(sep)
                else:
                    data = [data.replace(' ', '-')]

                header = header[5:]
                for val in data:
                    self.add_tags(message, 'rt/{}/{}'.format(header, val))
