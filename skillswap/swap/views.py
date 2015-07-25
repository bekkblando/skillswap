from django.shortcuts import render_to_response
from swap.models import Skill
from rest_framework import generics
from rest_framework import serializers
from rest_framework import filters


def home(request):
    return render_to_response("home.html")


def add_skill(request):
    return render_to_response("knowskill.html")





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