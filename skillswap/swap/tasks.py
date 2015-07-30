from __future__ import absolute_import
from datetime import timedelta
from .models import Skill, Profile
from .recommend import load_dataset, createC1, scanD, aprioriGen
import os

from celery import Celery, task

from celery import shared_task

from skillswap.celery import app


@app.task(name='tasks.recommend')
def recommend():
    skilllist = Skill.objects.all()
    #learnvalues = [abs(hash(item.name)) for item in skilllist]
    lookupvalues = {abs(hash(item.name)):item for item in skilllist}
    learnset = []
    profiles = Profile.objects.all()
    for item in profiles:
        learn = item.learn.all()
        if len(learn):
            learnset.append([abs(hash(item.name)) for item in learn])
    dataset = load_dataset(learnset)
    C1 = list(createC1(dataset))
    D = list(map(set, dataset))
    L1,support_data = scanD(D,C1,0.5)
    learnrules = aprioriGen(L1, 2)
    itemlearnsets = []
    for item in learnrules:
        numberset = list(item)
        itemlearnsets.append([lookupvalues[numberset[0]], lookupvalues[numberset[1]]])
    testing=[]
    for profile in profiles:
        for rules in itemlearnsets:
            testing.append(rules)
            if rules[0] in profile.learn.all() and not rules[1] in profile.learn.all() and not rules[0] in profile.skills.all() \
                and not rules[1] in profile.skills.all() and not rules[1] in profile.recommendation.all():
                print(profile)
                profile.recommendation.add(rules[1])
                #testing.append((profile.recommendation.all(), profile))
        profile.save()
    return testing
