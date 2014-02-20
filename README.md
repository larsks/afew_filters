This is a collection of filters for use with [afew][], a post-fetch
tagging tool that works with [notmuch][].

To use these filters, copy them into `~/.config/afew/`.

Note that at the moment these will only work with my [forked version
of afew][larsks] due to some missing functionality in the original
version.

[afew]: https://github.com/teythoon/afew
[notmuch]: http://notmuchmail.org/
[larsks]: https://github.com/larsks/afew

## The Filters

- BugzillaFilter.py

    - Sets tags `bug` and `bug/<bugid>`
    - Extracts `X-Bugzilla` headers into `bz/<header>/<value>` tags:

        - bz/classification
        - bz/component
        - bz/flags
        - bz/information-type
        - bz/priority
        - bz/private
        - bz/product
        - bz/reason
        - bz/security-vulnerability
        - bz/severity
        - bz/status
        - bz/triaged
        - bz/type
        - bz/watch-reason

- GerritFilter.py

    - Sets tags `bug` and `bug/<bugid>`
    - Extracts `X-Gerrit` headers into `gerrit/<header>/<value>` tags.

- LaunchpadFilter.py

    - Sets tags `bug` and `bug/<bugid>`
    - Extracts `X-Launchpad` headers into `lp/<header>/<value>` tags:

        - lp/information-type/
        - lp/private/
        - lp/security-vulnerability/
        - lp/tags/

- CustomListTagsFilter.py
- MailmanFilter.py
- MultiHeaderFilter.py
- RTFilter.py
