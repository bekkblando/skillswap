from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length = 140)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Skill {}".format(self.name)


class Profile(models.Model):
    user = models.OneToOneField(User)
    skills = models.ManyToManyField(Skill, through="SkillKnow", related_name='skills')
    learn = models.ManyToManyField(Skill, through="SkillLearn", related_name='learn')
    address = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], blank=True, max_length=18) # validators should be a list

    def __str__(self):
        return "Username {}, address {}, Skills {}, learn {}".format(self.user, self.address, self.skills, self.learn)

class SkillKnow(models.Model):
    rank = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(Profile)
    skill = models.ForeignKey(Skill)

    def __str__(self):
        return "Rank {}, description {}, user {}, skill {}".format(self.rank, self.description, self.user, self.skill)

class SkillLearn(models.Model):
    rank = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(Profile)
    skill = models.ForeignKey(Skill)

    def __str__(self):
        return "Rank {}, description {}, user {}, skill {}".format(self.rank, self.description, self.user, self.skill)

class Meeting(models.Model):
    meeting = models.TextField()
    usercommenting = models.ForeignKey(Profile, related_name="commenter")
    usercommentedon = models.ForeignKey(Profile, related_name="commentedon")

    def __str__(self):
        return "How {}, user commenting {}, usercommented on {}".format(self.meeting, self.usercommenting, self.usercommentedon)
