from django.contrib import admin

from swap.models import Skill, SkillKnow, SkillLearn, Meeting, Profile, UserChat, Message
# Register your models here.


admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(SkillKnow)
admin.site.register(SkillLearn)
admin.site.register(Meeting)
admin.site.register(UserChat)
admin.site.register(Message)
