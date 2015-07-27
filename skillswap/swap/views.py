from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import DeleteView, DetailView
from swap.models import Skill, Profile, SkillLearn, SkillKnow
from rest_framework import generics
from rest_framework import serializers
from rest_framework import filters
from swap.forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):
    return render_to_response("home.html", context_instance=RequestContext(request))


@login_required(redirect_field_name='login')
def profile(request):
    context = {}
    know = []
    learn = []
    exact = []
    smatch = []
    simmatch = []
    profile = Profile.objects.get(user = request.user)
    context['address'] = profile.address
    context['phone'] = profile.phone
    knowall = profile.skills.all()
    learnall = profile.learn.all()
    for item in knowall:
        know.append(SkillKnow.objects.get(user=profile, skill=item))
    for ite in learnall:
        learn.append(SkillLearn.objects.get(user=profile, skill=ite))
        match = Profile.objects.filter(skills__in = [ite] )
        skillsvalue = Profile.objects.all().values_list('skills__name')
        for item in skillsvalue:
            skillname = str(item[0])
            mat = skillname.find(ite.name)
            if mat != -1:
                skil = Skill.objects.get(name=item[0])
                simmatch = Profile.objects.filter(skills__in = [skil])
        if len(match):
            exact.append((ite, match))
        if len(simmatch) and not skil in exact and item[0] != None:
            print(skil)
            smatch.append((item, simmatch, skil))
    context['exact'] = exact
    context['learn'] = learn
    context['know'] = know
    context['similiar'] = smatch

    return render_to_response("profile.html", context, context_instance=RequestContext(request))


@login_required(redirect_field_name='login')
def add_skill(request):
    context = {}
    print(request.user)
    profile = Profile.objects.get(user = request.user)
    if request.POST:
        print("YO")
        print(request.user)
        skilltype = request.POST['skill']
        name = request.POST['name'].lower()
        try:
            eskill = Skill.objects.get(name=name)
        except:
            eskill = Skill.objects.create(name=name)
        description = request.POST['description']
        print(eskill)
        if eskill:
            profile = Profile.objects.get(user = request.user)
            if skilltype == "learn":
                if not eskill in profile.learn.all() and not eskill in profile.skills.all():
                    addskill = SkillLearn.objects.create(description=description, user=profile, skill=eskill)
                    addskill.save()
            if skilltype == "know":
                if not eskill in profile.skills.all() and not eskill in profile.learn.all():
                    rank = request.POST['rank']
                    addskill = SkillKnow.objects.create(rank = rank , description=description, user=profile, skill=eskill)
                    addskill.save()
        else:
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



def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

class KnowDeleteView(DeleteView):
    model = SkillKnow
    success_url = reverse_lazy("profile")

class LearnDeleteView(DeleteView):
    model = SkillLearn
    success_url = reverse_lazy("profile")

class UserPageView(DetailView):
    model = Profile
    template_name = 'userpage.html'
    
    def get_context_data(self, **kwargs):
        context = super(UserPageView, self).get_context_data()
        knowall = []
        learnall = []
        know = context['profile'].skills.all()
        learn = context['profile'].learn.all()
        for skill in know:
            knowall.append((skill.name, SkillKnow.objects.get(user=context['profile'], skill=skill)))
        for skill in learn:
            learnall.append((skill.name, SkillLearn.objects.get(user=context['profile'], skill=skill)))
        context['know'] = knowall
        context['learn'] = learnall
        print(context)
        return context


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