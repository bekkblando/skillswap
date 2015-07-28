from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class Skill(models.Model):
    name = models.CharField(max_length = 140)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Skill {}".format(self.name)


class Profile(models.Model):
    user = models.OneToOneField(User)
    skills = models.ManyToManyField(Skill, through="SkillKnow", related_name='skills')
    learn = models.ManyToManyField(Skill, through="SkillLearn", related_name='learn')
    streetnumber = models.IntegerField()
    street = models.CharField(max_length=140)
    city = models.CharField(max_length=140)
    state = models.CharField(max_length=2)
    created = models.DateTimeField(auto_now_add=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], blank=True, max_length=18) # validators should be a list

    def __str__(self):
        return "{}".format(self.user)

class SkillKnow(models.Model):
    rank = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(Profile)
    skill = models.ForeignKey(Skill)

    def __str__(self):
        return "Rank {}, description {}, user {}".format(self.rank, self.description, self.user)

class SkillLearn(models.Model):
    # rank = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(Profile)
    skill = models.ForeignKey(Skill)

    def __str__(self):
        return "description {}, user {}".format(self.description, self.user)

class Meeting(models.Model):
    meeting = models.TextField()
    usercommenting = models.ForeignKey(Profile, related_name="commenter")
    usercommentedon = models.ForeignKey(Profile, related_name="commentedon")

    def __str__(self):
        return "How it went: {}, user commenting: {}, usercommented on: {}".format(self.meeting, self.usercommenting, self.usercommentedon)


class UserChat(models.Model):
    user1 = models.ForeignKey(Profile, related_name="user1")
    user2 = models.ForeignKey(Profile, related_name="user2")
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Chat, User1: {} , User2: {}".format(self.user1, self.user2)

class Message(models.Model):
    text = models.CharField(max_length=300)
    chat = models.ForeignKey(UserChat)
    sender = models.ForeignKey(Profile)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['datetime']


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)