MediaTagi Admin
===============

To the largest extent possible, necessary administrative tasks (like suppressing vandalism or managing user capabilities) should be done by applying 'functional' tags that have special impact on the display or interpretation of other tags. 

Such 'functional' tags will be recognizable by their syntax (such as reserved starting characters). Use of some such tags may only have effect when applied by some users, and the management of such privileges should itself be bootstrapped by tag applications. 

Functional tags should be available to the widest possible number of users, and even where a user does not have the requisite privileges to apply tags with immediate effect, they should be able to apply them as inert 'recommendations' or 'rehearsals'. 

Examples
--------

*Negation*, with a `-` prefix, asserts that the following tag should not apply. For example, if one user tags a work with `:profanity`, and a later user believes the work does not (by the reference policy) qualify for the `:profanity` tag, the later user may add a `-:profanity` tag. In some summary views (those where last contribution of type prevails, as with last-edit-wins in wikis), that would mean the `:profanity` tag does not display. Simple negation is available to all users. 

*Override* (or 'lock'), with a double-colon (`::`) prefix, asserts that regardless of other ways to choose the displayed version of a tag with contradictory contributions (favor first, favor most, favor last, etc.), this variant should be preferred in default summaries. For example, a `::profanity` tag would ensure that `:profanity` appears in a summary view, regardless of later `-:profanity` tags. (A later `::` override would however take precedence.)

Only a subset of trusted users, like Wikipedia Sysops, would have their override tags respected. Ideally, there would be many such users, but the casual use of override would be discouraged, reserved for use against egregious abuse or to lock trivial uncontroversial values in place. 

Potentially, some users could be given conditional override privileges, for only a subset of tag types, tag values, or target works. For example, an author might be given blanket override privileges to mark targets as their own works of authorship, eg: `::author: Nicolas Bourbaki`. They could then also be given free reign to override other tags on those so-marked works (but not other works by other authors). 

*Reflexivity*, with a `{` prefix, asserts the the tag applies to the tvent itself, rather than the tvent's other target. Thus a compact inline characterization of the tvent is possible, without relying on a second tvent. For example, a tvent that itself has `:profanity`, even if somehow the target work does not, could include the reflexive tvent tag `{:profanity`.

Graduated Visibility
--------------------

*Fading*, applied with `:fade`, is typically applied to a tvent and prevents general viewing or inclusion in summaries. Still, by requesting to see faded tvents, any user can see them, and they may even be shown by default (with special decoration) to the user whose tvent is the target, or the user who applied the tag. Essentially, it is the mildest form of moderation, used to clean up after honest mistakes and other minor problems. 

*Squelching*, applied with `:squelch`, works like fading but makes a tvent generally invisible, and there is no way to request viewing of squelched tvents. Only the user who made the target tvent, the user who applied the squelch, and certain privileges sysops/admins can see a squelched tvent. It is effectively a deletion of the tvent, but with a audit record of the action. 

Any user may delete, fade, squelch, or delete their old tvents, or any individual tag inside them. Users with added privileges will be able to effectively fade or squelch other events. Actions may include an explanatory comment, typically as a reflexive `{comment:` tag. 

An 'inert' fade or squelch (made by users with no special privileges) serves as a sort of 'flag' to be considered by other users who could make the action take effect. 

*Blessing*, applied with `:bless`, transfers the applying users' privileges to the target tvent. It essentially says, I concur, thank you, let this take effect. Similarly, `:unbless` renders a previously active action inert. 

TK extended example:
- bad tvent
- unpriv user fades
- priv user blesses

Larger Constraints
------------------

(?) *Sleeving*, applied with `:sleeve`, typically applied to a target, implies certain policy-based limits on the collection and display of information about that target, for reasons of legality/propriety. (TBD: What limits? Are finer gradiations required?) 

(TBD) Some subset of tags (eg: `:mature`, `:offensive`, `:pornographic`, or others to be discussed) may cause target summaries, tvents, or tvent log views to only be visible under certain conditions. Conditions might include: registered user of above a certain age; interstitial clickthrough acceptance of a warning; only viewable on segregated alternate domain; etc.

