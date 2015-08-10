from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
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
        return "{}".format(self.name)

states = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'),
           ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'),
           ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'),
           ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'),
           ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'),
           ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'),
           ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
           ('NC', 'North Carolina'),('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
           ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'),
           ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]
gender = [('Female', 'Female'), ('Male', 'Male')]
class Profile(models.Model):
    user = models.OneToOneField(User)
    skills = models.ManyToManyField(Skill, through="SkillKnow", related_name='skills')
    learn = models.ManyToManyField(Skill, through="SkillLearn", related_name='learn')
    streetaddress = models.CharField(max_length=140, blank=True)
    city = models.CharField(max_length=140, blank=True)
    state = models.CharField(max_length=2, blank=True, choices=states)
    zipcode = models.CharField(max_length=5, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    phone_regex = RegexValidator(regex=r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], blank=True, max_length=18) # validators should be a list
    recommendation = models.ManyToManyField(Skill, related_name="recommend")
    gender = models.CharField(max_length=7, blank=True, choices=gender)
    age = models.IntegerField(validators=[MinValueValidator(13), MaxValueValidator(120)], null=True)


    @property
    def geo_enabled(self):
        if self.streetaddress and self.city and self.state and self.zipcode:
            print(self.streetaddress ,self.city , self.state , self.zipcode)
            return True
        else:
            print(self.streetaddress ,self.city , self.state , self.zipcode)
            print("Fail")
            return False

    def __str__(self):
        return "{}".format(self.user)

class SkillKnow(models.Model):
    rank = models.CharField(max_length=15)
    description = models.TextField()
    user = models.ForeignKey(Profile)
    skill = models.ForeignKey(Skill)

    def __str__(self):
        return "Rank {}, description {}, user {}".format(self.rank, self.description, self.user)

class SkillLearn(models.Model):
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