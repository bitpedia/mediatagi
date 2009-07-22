from django.http import HttpResponse
import urllib
from djmediatagi.tvents.models import Tvent
from datetime import datetime
from django.shortcuts import render_to_response
from models import TagSummary, FieldSummary, to_datetime, Target
import sys

def home(request):
    return render_to_response("base.html",{})

def bzpull(request, target):
    """Pull tvents from bitzi.com for given bitprint."""
    tventtxt = urllib.urlopen("http://bitzi.com/lookup/%s?v=tventtxt" % target)
    tventdict = {}
    targets_to_update = set()
    count = 0
    text = ""
    try:
        for line in tventtxt:
            text += '\n'
            line = line.strip()
            text += line
            if not line:
                if 'user' in tventdict and 'target_id' in tventdict and 'when' in tventdict:
                    tvent = Tvent()
                    tvent.when = tventdict['when']
                    tvent.user = tventdict['user']
                    target, created = Target.objects.get_or_create(id=tventdict['target_id'])
                    tvent.target = target
                    targets_to_update.add(target.id)
                    tvent.tagtext = tventdict['tagtext']
                    tvent.save()
                    count += 1
                else:
                    # error; required field not present
                    text += '\nERROR: incomplete tvent ' + str(tventdict)
                tventdict = {}
                continue
            if line.startswith("="):
                tventdict['when'] = line[1:]
                continue
            if line.startswith("~"):
                tventdict['user'] = line[1:]
                continue
            if line.startswith("@"):
                tventdict['target_id'] = line[1:]
                continue
            tventdict['tagtext'] = tventdict.get('tagtext','') + line + '\n'
        if 'user' in tventdict and 'target_id' in tventdict and 'when' in tventdict:
            # TODO: reduce duplication with above
            tvent = Tvent()
            tvent.when = tventdict['when']
            tvent.user = tventdict['user']
            target = Target.objects.get_or_create(id=tventdict['target_id'])
            tvent.target = target
            targets_to_update.add(target.id)
            tvent.save()
            count += 1
        else:
            # error; required field not present
            text += '\nERROR: incomplete tvent ' + str(tventdict)
    finally:
        tventtxt.close()
    # trigger update of any possibly-changed Target summaries
    for id in targets_to_update:
        Target.objects.get(id=id).updateFromTvents()
    return HttpResponse('Pulled %d tvents from:\n %s' % (count, text), mimetype='text/plain')

def log(request, tag=''):
    """Display a revchron log of Tvents (all or matching 'tag')"""
    tvents = Tvent.objects
    if tag:
        if tag.startswith("~"):
            tvents = tvents.filter(user=tag[1:])
        elif tag.startswith("@"):
            tvents = tvents.filter(target=tag[1:])
        else:
            # TODO: other log types?
            pass
    try:
        until = to_datetime(request.GET['until'])
        tvents = tvents.filter(datetime__lte=until)
    except (KeyError, ValueError):
        until = ''

    tvents = tvents.order_by('-datetime')
    tvents.select_related('target')
    # output = '\n\n'.join([tv.uniqey + '\n'.join([str(s) for s in tv.tags]) for tv in tvents])
    return render_to_response('log.html',{'tvents':tvents, 'until':until, 'tag':tag})

# default groupings of consensus fields for Target summaries
# TODO: move? offer different groupings for another view?
tag_groups = [ ( '',
                 [':filename:', ':length:', ':mediatype:', ':title:', ':creator:',]),
               ( 'media details',
                 [':duration:', ':format:', ':dimensions:', ':bitrate:', ':sampling:', ':codec:',
                  ':fps:', ':framerate:', ':height:', ':width:',]),
               ( 'reference identifiers',
                 [':tree:', ':tigertree:', ':ed2khash:', ':kzhash:', ':md5:', 'crc32:',
                  ':first20:',]),
              ]

def summary(request, tag=''):
    """Display an organized summary of fieldvalues and tag frequency."""
    if tag:
        if tag.startswith("@"):
            target = Target.objects.get(id=tag[1:])
            summaries_by_value, consfield_summaries = target.getSummaries()
        elif tag.startswith("~"):
            # TODO: is there a sensible analogous summary for users,
            # or does it look completely different? 
            pass
        else:
            # TODO: other log types
            pass

    # replace fieldnames in tag_groups with fieldsummaries in grouped_summaries
    grouped_summaries = [ ( gtuple[0], [ summaries_by_value.pop(t) for t in gtuple[1] if t in summaries_by_value])
                          for gtuple in tag_groups ]
    # add misc consensus fields
    grouped_summaries.append(('other consensus fields',
                          [ summaries_by_value.pop(k) for k in summaries_by_value.keys()
                            if summaries_by_value[k].is_consensus and summaries_by_value[k].fieldname ]))
    # add misc consensus labels
    grouped_summaries.append(('consensus labels',
                          [ summaries_by_value.pop(k) for k in summaries_by_value.keys()
                            if summaries_by_value[k].is_consensus]))
    grouped_summaries[-1][-1].sort(lambda x,y:cmp(x.count,y.count))
    # add misc adhoc fields
    grouped_summaries.append(('adhoc fields',
                          [ summaries_by_value.pop(k) for k in summaries_by_value.keys()
                            if summaries_by_value[k].fieldname ]))
    grouped_summaries[-1][-1].sort(lambda x,y:cmp(x.count,y.count))
    # add misc adhoc labels
    grouped_summaries.append(('adhoc labels',
                          [ summaries_by_value.pop(k) for k in summaries_by_value.keys()]))
    grouped_summaries[-1][-1].sort(lambda x,y:cmp(x.count,y.count))
    
    return render_to_response('summary.html',{'grouped_summaries':grouped_summaries, 'consfield_summaries':consfield_summaries, 'tag':tag})

def addtags(request, target_id):
    if target_id:
        target = Target.objects.get(pk=target_id)
    else:
        target = None

    return render_to_response("addtags.html",{'target':target})
        
