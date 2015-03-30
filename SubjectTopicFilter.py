from __future__ import print_function, absolute_import, unicode_literals

import re

from afew.filters.BaseFilter import Filter
from afew.FilterRegistry import register_filter

re_topic = re.compile('\[(?P<tag>[^\]]*)\]')


@register_filter
class SubjectTopicFilter(Filter):
    message = 'Extracting tags from subject'

    def handle_message(self, message):
        if not message.get_header('subject'):
            return

        topics = re_topic.findall(message.get_header('subject'))
        if hasattr(self, 'exclude'):
            exclude_topics = set(self.exclude.split(';'))
        else:
            exclude_topics = set()

        for topic in topics:
            if topic in exclude_topics:
                continue

            self.remove_tags(message, 'topic/%s' % topic)
            self.add_tags(message, 'topic/%s' % topic.lower())
