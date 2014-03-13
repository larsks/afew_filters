from __future__ import print_function, absolute_import, unicode_literals

import os
import re
import fnmatch

from afew.filters.BaseFilter import Filter
from afew.FilterRegistry import register_filter

subject_re = re.compile('\[(?P<pkgspec>(?P<package>[^/\]]+)(/(?P<target>[^\]]+))?)\] .*')

@register_filter
class DistGitFilter(Filter):
    message = 'Processing dist-git messages'
    query = "to:cvs-commits-list"

    def handle_message(self, message):
        mo = subject_re.match(message.get_header('subject'))

        if mo:
            this_package = mo.group('package')
            this_pkgspec = mo.group('pkgspec')
            for pattern in self.packages.split(';'):
                if '/' in pattern and fnmatch.fnmatch(this_pkgspec,
                                                      pattern):
                    break
                elif fnmatch.fnmatch(this_package, pattern):
                    break
            else:
                try:
                    os.unlink(message.get_filename())
                    self.database.remove_message(message.get_filename())
                    self.log.warn('Deleted commit message id:%s for package %s' % (
                        message.get_message_id(),
                        this_package))
                except OSError, detail:
                    self.log.warn('Failed to delete message id:%s: %s' % (
                        message.get_message_id(),
                        detail))

