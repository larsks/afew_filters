from __future__ import print_function, absolute_import, unicode_literals

from afew.filters.BaseFilter import Filter
from afew.FilterRegistry import register_filter


@register_filter
class CustomListTagsFilter(Filter):
    message = 'Applying custom list tags'
    unmatched_tag = 'latent'

    def __init__(self, database, **kwargs):
        self.lists = {}

        for k, v in kwargs.items():
            if not hasattr(self, k):
                self.lists[k] = v.split(';')
                del kwargs[k]

        super(CustomListTagsFilter, self).__init__(database, **kwargs)

    def handle_message(self, message):
        matched = False
        value = message.get_header('list-id').lower()
        if not value:
            return

        for listid, tags in self.lists.items():
            if listid in value:
                self.add_tags(message, *tags)
                matched = True

        if not matched:
            self.add_tags(message, self.unmatched_tag)
