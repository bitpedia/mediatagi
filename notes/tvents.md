MediaTagi Tag Syntax & Tvents
=============================

Tag Syntax
----------

Tags may include any unicode characters.

Tags beginning with `:` (a colon) should conform to consensus interpretations, as defined in the corresponding reference wiki. (Tags not beginning with a colon mean no more and no less than the individual user intends, as with other systems.)

For example, the tag `:mature` would mean what the corresponding reference wiki page `:mature` defines it to mean. (For example, that the tag target contains content intended for a non-child audience, according to discussed and documented standards.) In contrast, the plain tag `mature` may mean different things to different users, as with various personal/bookmark tagging systems.

Tags with an infix colon are considered `fielded` tags. (For example, `:title: Harry Potter and the Sorcerer's Stone` or `:author: J. K. Rowling`, which are each also consensus-interpretation tags, by the leading colon.)

The interface will provide special summaries of consensus tagging, such as the counts and times of earliest/latest application of each tag, or of the first/most-commonly/last provided values for fields.

As many administrative/moderation tasks as possible will be achieved by tagging ('functional tags'). Thus some tag syntax, other than just a preceding colon, will have special meaning to the system, such as overriding previous tags.

Tvents
------

Multiple tags applied at the same moment, by the same user, to the same target are collected in a batch called a 'tagging event' or 'tvent' for short.

That is, a tvent includes a (single) target, a (single) originating user, a (single, current) timestamp, and some number of tags (of any sort).

Tvents are representable in plain Unicode text. In this representation, even the target, originating user, and timestamp can be seen as tags of a special syntax. The target is prefixed with a `@`; the user with a `~`; the timestamp with a `=`. Tags are ended with a CR; a CR may be included in the tag by backslash-escaping. Tvents are ended with a blank line. (The empty string is not a legal tag.)

Tvents have their own URIs, and are themselves taggable. The URI scheme is `tvent`, and the timestamp, user, and target appear in order, each preceded by a `/` path-separator. For example, a URI to a specific tvent, relative within a mediatagi site could be:

    tvent:/=2008-12-15T22:07:49/~gojomo/@sha1:WFVZH63UI4NBKYROQWLISCXXY2H5KNNL

(An absolute tvent URI distinguishing among alternate sites can add an `//authority.com` portion immediately after the scheme.)


Examples
--------

These are two tvents by two users against the same target within a few minutes of each other:

    =2008-12-15T22:07:49
    ~gojomo
    @sha1:WFVZH63UI4NBKYROQWLISCXXY2H5KNNL
    :movie
    :filename: NightOfTheLivingDead.ogv
    :length: 411906346
    :title: Night of the Living Dead
    :director: George A. Romero
    :date: 1968
    :source url: http://www.archive.org/download/NightOfTheLivingDead-MPEG/NightOfTheLivingDead.ogv
    
    =2008-12-15T22:08:22
    ~horrorfan
    @sha1:WFVZH63UI4NBKYROQWLISCXXY2H5KNNL
    zombies
    black and white
    :filename: Night of the Living Dead.ogv
    :mimetype: video/ogg
    :licensing: public domain

MediaTagi will import tvents in this format, subject to checks on whether the source is trusted to provide timestamps and usernames.
