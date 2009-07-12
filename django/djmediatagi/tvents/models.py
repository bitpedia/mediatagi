from django.db import models
from datetime import datetime
from collections import defaultdict

def to_datetime(ts):
    """Takes a datetime or string in various forms, returns datetime"""
    if(isinstance(ts,datetime)):
        return ts
    elif(isinstance(ts,str)):
        return datetime.strptime(ts.rstrip('Z'),"%Y-%m-%dT%H:%M:%S")
    else:
        raise(TypeError)

class Target(models.Model):
    """Summary of information for one target"""

    id = models.CharField(max_length=256,primary_key=True)
    name_first = models.CharField(max_length=1024,default='');
    name_first_tvent_first = models.ForeignKey('Tvent', related_name='firstnamefor',null=True)
    name_last = models.CharField(max_length=1024,default='')
    name_last_tvent_last = models.ForeignKey('Tvent', related_name='lastnamefor',null=True)
    name_most = models.CharField(max_length=1024,default='')
    name_most_tvent_first = models.ForeignKey('Tvent', related_name='mostnamefor',null=True)
    
    def getSummaries(self):
        """Return dictionaries of all summaries (by raw field-name or label)
        and consensus field summaries (by field-name shorn of ':')"""
        
        tvents = Tvent.objects.filter(target=self.id).order_by('-datetime')
        all_summaries = {}
        for tv in tvents:
            for t in tv.tags:
                key = t.fieldname or t.value
                if not key in all_summaries:
                    all_summaries[key] = FieldSummary(key) if t.fieldname else TagSummary(key)
                all_summaries[key].addTag(t)
        consfield_summaries = dict([ (k.strip(':'), all_summaries[k])
                                          for k in all_summaries.keys()
                                          if (k.startswith(':') and k.endswith(':')) ])
        return all_summaries, consfield_summaries

    def updateFromTvents(self):
        """Update DB fields for first, most, last filename"""
        
        all_summaries, consfield_summaries = self.getSummaries()
        filenamesummary = consfield_summaries['filename']
        if not filenamesummary:
            return
        self.name_first = filenamesummary.first.fieldvalue
        self.name_first_tvent_first = filenamesummary.first.tvent
        self.name_last = filenamesummary.last.fieldvalue
        self.name_last_tvent_last = filenamesummary.last.tvent
        most = filenamesummary.findmost()
        self.name_most = most.fieldvalue
        self.name_most_tvent_first = most.first.tvent
        self.save()
        
class Tvent(models.Model):
    """One tagging event, featuring a timestamp, user, target, and tags.

    The primary key, uniqey, is synthesized from timestamp+user+target_id.
    
    """
    datetime = models.DateTimeField()
    user = models.CharField(max_length=32, db_index=True)
    target = models.ForeignKey(Target)
    # synth primary key: '=' iso-date + '/~' + user + '/@' + target
    uniqey = models.CharField(max_length=(1+19+1+user.max_length+1+256), primary_key=True)
    tagtext = models.TextField(max_length=1024)

    def __update_uniqey(self):
        """update the primary key when other attributes change"""
        try:
            self.uniqey = "=" \
                          + self.when \
                          + "/~" \
                          + self.user \
                          + "/@" \
                          + self.target_id
        except (AttributeError, TypeError):
            self.uniqey = ""

    def __setattr__(self, name, value):
        """trigger uniqey update"""
        models.Model.__setattr__(self, name, value)
        if name in ('when','user','target_id'):
            self.__update_uniqey()
    
    def __unicode__(self):
        return self.uniqey

    @property
    def tags(self):
        """return list of Tag instances from tagtext"""
        return [ Tag(t.strip(), self) for t in self.tagtext.splitlines() ]

    @property
    def when(self):
        """return iso8601 string of timestamp"""
        return self.datetime.isoformat().split(".")[0]

    @when.setter
    def when(self, value):
        """allow timestamp set by datetime or iso8601 string"""
        self.datetime = to_datetime(value)

class Tag():
    """a single tag inside a Tvent"""
    
    def __init__(self, value, tvent):
        self._value = value
        self.tvent = tvent

    @property
    def value(self):
        """full string value of tag"""
        return self._value

    @property
    def when(self):
        """timestamp of tag, pulled from Tvent"""
        return self.tvent.when

    @property
    def user(self):
        """user contributor of tag, pulled from Tvent"""
        return self.tvent.user

    @property
    def target(self):
        """target of tag, pulled from Tvent"""
        return self.tvent.target
    
    @property
    def is_consensus(self):
        """true if tag begins with ':' consensus-def indicator"""
        return self._value.startswith(':')
    
    @property
    def fieldname(self):
        """extracts fieldname if tag has interior ':'"""
        index = self._value.find(':',1)
        return self._value[:index+1] if index > 0 else None

    @property
    def fieldvalue(self):
        """extracts fieldvalue if tag has interior ':'"""
        index = self._value.find(':',1)
        return self._value[index+1:].strip() #if index > 0 else None

    def __unicode__(self):
        return self._value
    
class TagSummary():
    """summary of a tag's applications, with count, first, last"""
    
    def __init__(self, key):
        self.userwhen = {}
        self.value = key
        self.first = None
        self.last = None
        self.count = 0

    @property
    def count(self):
        return self.count
    
    @property
    def fieldvalue(self):
        return self.first.fieldvalue

    @property
    def fieldname(self):
        return self.first.fieldname

    @property
    def is_consensus(self):
        return self.first.value.startswith(':')

    def addTag(self, tag):
        """tally a tag into the running summary

        Only the latest tag from the same user is counted,

        """
        if not tag.value.startswith(self.value):
            raise ValueError
        if (tag.user in self.userwhen) and (self.userwhen[tag.user] > tag.when):
            return
        self.userwhen[tag.user] = tag.when
        self.count +=1
        if (not self.first) or (self.first.when > tag.when):
            self.first = tag
        if (not self.last) or (self.last.when < tag.when):
            self.last = tag

class FieldSummary(TagSummary):
    """TagSummary specialization that summarizes a fieldname's tags.

    Uses an internal dict of TagSummaries to tally each fieldvalue variant.
    
    """
    def __init__(self, key):
        TagSummary.__init__(self,key)
        self.fieldsummaries = {}

    def addTag(self, tag):
        """Creates, tallies per-fieldvalue TagSummaries by full tag"""
        TagSummary.addTag(self,tag)
        if len(tag.value) > len(self.value):
            if not tag.value in self.fieldsummaries:
                self.fieldsummaries[tag.value] = TagSummary(tag.value)
            self.fieldsummaries[tag.value].addTag(tag)

    @property
    def cardinality(self):
        """Count of unique fieldvalues"""
        return len(self.fieldsummaries.items())

    @property
    def variants(self):
        lastsummary =  self.fieldsummaries[self.last.value]
        mostsummary =  self.findmost()
        firstsummary = self.fieldsummaries[self.first.value]
        for summary in (lastsummary, mostsummary, firstsummary):
            summary.labels=[]
        lastsummary.labels.insert(0,'last')
        mostsummary.labels.insert(0,'most')
        firstsummary.labels.insert(0,'first')
        vars = []
        for summary in (lastsummary, mostsummary, firstsummary):
            if summary not in vars:
                vars.append(summary)
        return vars

    def findmost(self):
        """inner tagsummary corresponding to most-common tag"""
        candidate = self.last.value
        for k, ts in self.fieldsummaries.items():
            if ts.count > self.fieldsummaries[candidate].count:
                candidate = k
        return self.fieldsummaries[candidate]
