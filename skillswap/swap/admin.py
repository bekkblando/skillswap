from django.contrib import admin
from swap.models import Skill, SkillKnow, SkillLearn, Meeting, Profile
# Register your models here.


admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(SkillKnow)
admin.site.register(SkillLearn)
admin.site.register(Meeting)