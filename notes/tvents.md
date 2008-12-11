MediaTagi Tag Syntax & Tvents
=============================

Tag Syntax
----------

Tags may include any unicode characters.

Tags beginning with ':' (a colon) should conform to consensus interpretations, as defined in the corresponding reference wiki. (Tags not beginning with a colon mean no more and no less than the individual user intends, as with other systems.)

For example, the tag ':mature' would mean what the corresponding reference wiki page ':mature' defines it to mean. (For example, that the tag target contains content intended for a non-child audience, according to discussed and documented standards.) In contrast, the plain tag 'mature' may mean different things to different users, as with various personal/bookmark tagging systems.

Tags with an infix colon are considered 'fielded' tags. (For example, ':title: Harry Potter and the Sorcerer's Stone' or ':author: J. K. Rowling', which are each also consensus-interpretation tags, by the leading colon.)

The interface will provide special summaries of consensus tagging, such as the counts and times of earliest/latest application of each tag, or of the first/most-commonly/last provided values for fields.

As many administrative/moderation tasks as possible will be acheived by tagging ('functional tags'). Thus some tag syntax, other than just a preceding colon, will have special meaning to the system, such as overriding previous tags.

Tvents
------

Multiple tags applied at the same moment, by the same user, to the same target are collected in a batch called a 'tagging event' or 'tvent' for short.

That is, a tvent includes a target, a user, a timestamp, and some number of tags (of any sort).

Tvents themselves may be tagged.

Tvents are representable in plain Unicode text. In this representation, even the target, originating user, and timestamp can be seen as tags of a special syntax.

Tvents have their own URIs, and are themselves taggable.

Examples
--------

TK






