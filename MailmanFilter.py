from __future__ import print_function, absolute_import, unicode_literals

from afew.filters.BaseFilter import Filter
from afew.FilterRegistry import register_filter


@register_filter
class MailmanFilter(Filter):
    message = 'Tagging Mailman administrivia'
    tags = ['+listsub', '+flagged', '+inbox']

    def handle_message(self, message):
        if message.get_header('list-id'):
            h_subject = message.get_header('subject')
            h_from = message.get_header('from')

            if '-request' in h_from and 'confirm' in h_subject:
                super(MailmanFilter, self).handle_message(message)
