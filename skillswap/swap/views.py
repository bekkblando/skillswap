from django.shortcuts import render_to_response
from django.template import RequestContext
from swap.models import Skill, Profile, SkillLearn, SkillKnow
from rest_framework import generics
from rest_framework import serializers
from rest_framework import filters


def home(request):
    return render_to_response("home.html")


def add_skill(request):
    context = {}
    print(request.user)
    profile = Profile.objects.get(user = request.user)
    if request.POST:
        print("YO")
        print(request.user)
        skilltype = request.POST['skill']
        name = request.POST['name']
        eskill = Skill.objects.get(name=name)
        description = request.POST['description']
        print(eskill)
        if eskill:
            profile = Profile.objects.get(user = request.user)
            if skilltype == "learn":
                addskill = SkillLearn.objects.create(description=description, user=profile, skill=eskill)
                addskill.save()
            if skilltype == "know":
                rank = request.POST['rank']
                addskill = SkillKnow.objects.create(rank = rank , description=description, user=profile, skill=eskill)
                addskill.save()
    context['learn'] = profile.learn.all()
    context['know'] = profile.skills.all()
    return render_to_response("knowskill.html", context, context_instance=RequestContext(request))





###### API VIEWS

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['name']

class SkillLookup(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)