from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length = 140)
    created = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User)
    skills = models.ManyToManyField(Skill, through="SkillData", related_name='skills')
    learn = models.ManyToManyField(Skill, related_name='learn')
    address = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    phone = models.IntegerField(null=True)

class SkillData(models.Model):
    rank = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(Profile)
    skill = models.ForeignKey(Skill)

class Meeting(models.Model):
    meeting = models.TextField()
    usercommenting = models.ForeignKey(Profile, related_name="commenter")
    usercommentedon = models.ForeignKey(Profile, related_name="commentedon")
