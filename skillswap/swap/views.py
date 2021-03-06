from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from swap.models import Skill, Profile, SkillLearn, SkillKnow, UserChat, Message, Meeting
from rest_framework import generics
from rest_framework import serializers
from rest_framework import filters
from swap.forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
import requests
from rest_framework import status
import os
from haystack.query import SearchQuerySet
import re
from swap.tasks import chatemail

class UpdateProfile(UpdateView):
    model = Profile
    fields = ['streetaddress', 'city', 'state','zipcode', 'phone', 'gender', 'age']
    template_name = 'user_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


def skillpage(request, pk):
    context = {}
    skill = Skill.objects.get(id=pk)
    context['skill'] = skill
    context['knowskill'] = SkillKnow.objects.filter(skill=skill)
    return render_to_response('skillpage.html', context, context_instance=RequestContext(request))


def home(request):
    return render_to_response("home.html", context_instance=RequestContext(request))


@login_required(redirect_field_name='login')
def geo_skills(request):
    context = {}
    if request.POST:
        people = []
        peopleinarea = []
        skillsinarea = []
        complete = []
        distance = 0
        try:
            distancemax = request.POST['distance']
            distancemax = int(''.join(x for x in distancemax if x.isdigit()))
            profiles = Profile.objects.all()
            currentuser = Profile.objects.get(user=request.user)
            streetad = currentuser.streetaddress.strip().replace(' ', '+')
            API_KEY = os.environ.get('GOOGLE_API_KEY')
            currentuserdata = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='
                                            + streetad + ',' + currentuser.city + ',' + currentuser.state + '&key=' + API_KEY)
            currentusercords = str(currentuserdata.json()['results'][0]['geometry']['location']['lat']) + ',' + str(
                currentuserdata.json()['results'][0]['geometry']['location']['lng'])
            for profile in profiles:
                if profile != currentuser and profile.skills.all():
                    streetad = profile.streetaddress.strip().replace(' ', '+')
                    profiledata = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='
                                               + streetad + ',' + profile.city + ',' + profile.state + '&key=' + API_KEY)
                    try:
                        profilecords = str(profiledata.json()['results'][0]['geometry']['location']['lat']) + ',' + str(
                            profiledata.json()['results'][0]['geometry']['location']['lng'])
                        disdata = requests.get(
                            'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + currentusercords + '&destinations=' + profilecords + '&key=' + API_KEY)
                        if disdata.json()['rows'][0]['elements'][0]['status'] != 'ZERO_RESULTS':
                            distance = disdata.json()['rows'][0]['elements'][0]['distance']['text']
                            distance = re.findall("(\d+)", distance)[0]
                            miles = 0.62137 * float(distance)
                            if miles <= distancemax:
                                peopleinarea.append(profile)
                                skillsinarea.append(profile.skills.all())
                                people.append([profile, profile.skills.all()])
                    except:
                        pass
                context['radius'] = distancemax

                context['address'] = "{}, {}, {}, {}".format(currentuser.streetaddress, currentuser.city, currentuser.zipcode, currentuser.state)
            skillspeople = []
            if len(skillsinarea) > 1 and len(skillsinarea) != 0:
                skillsinarea = list(set([skill for skilllist in skillsinarea for skill in skilllist]))

            else:
                skillsinarea= skillsinarea[0]

            for skill in skillsinarea:
                skillspeople = []
                for profile in peopleinarea:
                    if skill in profile.skills.all():
                        skillspeople.append(profile)
                    skillspeople = list(set(skillspeople))
                complete.append([skill, skillspeople])
            context['people'] = complete
        except:
            pass
    return render_to_response("geo_skills.html", context, context_instance=RequestContext(request))


@login_required(redirect_field_name='login')
def profile(request):
    context = {}
    know = []
    learn = []
    addedsimskill = []
    exact = []
    smatch = []
    simmatch = []
    filteredsmatch = []
    recommend = []
    profile = Profile.objects.get(user=request.user)
    recommendation = profile.recommendation.all()
    knowall = profile.skills.all()
    learnall = profile.learn.all()
    if len(recommendation):
        for item in recommendation:
            if item not in learnall and item not in knowall:
                recommend.append(item)
        context['recommendation'] = recommend
    print(recommend)
    context['address'] = '{} {}, {} '.format(profile.streetaddress, profile.city, profile.state)
    context['phone'] = profile.phone
    for item in knowall:
        know.append(SkillKnow.objects.get(user=profile, skill=item))
    for ite in learnall:
        add = False
        learn.append(SkillLearn.objects.get(user=profile, skill=ite))
        match = Profile.objects.filter(~Q(user=profile.user), skills__in=[ite])
        skillsvalue = Profile.objects.all().values_list('skills__name')
        for item in skillsvalue:
            skillname = str(item[0])
            mat = list(SearchQuerySet().filter(content=ite.name))
            if len(mat) != 0:
                for item in mat:
                    skil = Skill.objects.get(id=item.pk)
                    simmatch = Profile.objects.filter(~Q(user=profile.user), skills__in=[skil])
                    add = True
                    if len(simmatch) and not skillname == ite.name and skillname != 'None' and add:
                        if not skil in addedsimskill:
                            skillobject = Skill.objects.get(name=skillname)
                            addedsimskill.append(skil)
                            smatch.append((ite, simmatch, skil, skillobject.id))
        if len(match):
            exact.append([ite, match])
    for sitem in smatch:
        print("SITEM", sitem)
        skillcheck = Skill.objects.get(name=sitem[2])
        checkexact = [item[0] for item in exact]
        knowcheck = [item for item in profile.skills.all()]
        learncheck = [item for item in profile.learn.all()]
        if skillcheck in checkexact or skillcheck in knowcheck or skillcheck in learncheck:
                pass
        else:
            filteredsmatch.append(list(sitem))
    print(filteredsmatch)
    try:
        filteredsmatch[0][1] = filteredsmatch[0][1][:5]
    except:
        pass
    try:
        exact[0][1] = exact[0][1][:5]
    except:
        pass

    context['exact'] = exact
    context['learn'] = learn
    context['know'] = know
    context['similiar'] = filteredsmatch

    return render_to_response("profile.html", context, context_instance=RequestContext(request))


@login_required(redirect_field_name='login')
def add_skill(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    if request.POST:
        try:
            skilltype = request.POST['skill']
            name = request.POST['name'].lower()
            if len(name):
                try:
                    eskill = Skill.objects.get(name=name)
                except:
                    eskill = Skill.objects.create(name=name)
                description = request.POST['description']
                if eskill in profile.recommendation.all():
                    profile.recommendation.remove(eskill)
                    profile.save()
                if eskill:
                    profile = Profile.objects.get(user=request.user)
                    if skilltype == "learn":
                        if not eskill in profile.learn.all() and not eskill in profile.skills.all():
                            addskill = SkillLearn.objects.create(description=description, user=profile, skill=eskill)
                            addskill.save()
                    if skilltype == "know":
                        if not eskill in profile.skills.all() and not eskill in profile.learn.all():
                            rank = request.POST['rank']
                            addskill = SkillKnow.objects.create(rank=rank, description=description, user=profile, skill=eskill)
                            addskill.save()
                else:
                    profile = Profile.objects.get(user=request.user)
                    if skilltype == "learn":
                        addskill = SkillLearn.objects.create(description=description, user=profile, skill=eskill)
                        addskill.save()
                    if skilltype == "know":
                        rank = request.POST['rank']
                        addskill = SkillKnow.objects.create(rank=rank, description=description, user=profile, skill=eskill)
                        addskill.save()
        except:
            pass
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
            return redirect('login')
        else:
            pass
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render_to_response(
        'register.html',
        {'user_form': user_form, 'profile_form':profile_form, 'registered': registered},
        context)


def knowdelete(request, pk):
    if request.POST:
        profile = Profile.objects.get(user=request.user)
        knowskill = SkillKnow.objects.get(user=profile, skill_id=pk)
        knowskill.delete()
        return redirect('addskill')


def learndelete(request, pk):
    if request.POST:
        profile = Profile.objects.get(user=request.user)
        learnskill = SkillLearn.objects.get(user=profile, skill_id=pk)
        learnskill.delete()
        return redirect('addskill')

def addlearn(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    if request.POST:
        skilltype = request.POST['skill']
        name = request.POST['name'].lower()
        try:
            eskill = Skill.objects.get(name=name)
        except:
            eskill = Skill.objects.create(name=name)
        description = request.POST['description']
        if eskill in profile.recommendation.all():
            profile.recommendation.remove(eskill)
            profile.save()
        if eskill:
            profile = Profile.objects.get(user=request.user)
            if skilltype == "learn":
                if not eskill in profile.learn.all() and not eskill in profile.skills.all():
                    addskill = SkillLearn.objects.create(description=description, user=profile, skill=eskill)
                    addskill.save()
            if skilltype == "know":
                if not eskill in profile.skills.all() and not eskill in profile.learn.all():
                    rank = request.POST['rank']
                    addskill = SkillKnow.objects.create(rank=rank, description=description, user=profile, skill=eskill)
                    addskill.save()
        else:
            profile = Profile.objects.get(user=request.user)
            if skilltype == "learn":
                addskill = SkillLearn.objects.create(description=description, user=profile, skill=eskill)
                addskill.save()
            if skilltype == "know":
                rank = request.POST['rank']
                addskill = SkillKnow.objects.create(rank=rank, description=description, user=profile, skill=eskill)
                addskill.save()
        page = request.POST['page']
        return redirect('userpage/'+page+'/')

class UserPageView(DetailView):
    model = Profile
    template_name = 'userpage.html'

    def get_context_data(self, **kwargs):
        context = super(UserPageView, self).get_context_data()
        knowall = []
        learnall = []
        profile = kwargs['object']
        reviews = Meeting.objects.filter(usercommentedon=profile)
        print(reviews)
        know = context['profile'].skills.all()
        learn = context['profile'].learn.all()
        for skill in know:
            knowall.append((skill.name, SkillKnow.objects.get(user=context['profile'], skill=skill)))
        for skill in learn:
            learnall.append((skill.name, SkillLearn.objects.get(user=context['profile'], skill=skill)))
        context['review'] = reviews
        context['know'] = knowall
        context['learn'] = learnall
        return context


class ChatListView(ListView):
    model = UserChat
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['token'] = Token.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return UserChat.objects.filter(Q(user1=profile) | Q(user2=profile))


def userchatview(request):
    if request.POST:
        profile1 = Profile.objects.get(user=request.user)
        profile2 = Profile.objects.get(user__username=request.POST['user2'])
        if not UserChat.objects.filter(user1=profile1, user2=profile2) and not UserChat.objects.filter(user1=profile2,
                                                                                                user2=profile1):

            chat = UserChat.objects.create(user1=profile1, user2=profile2)
            chat.save()
            content = "New Chat Created With " + str(profile1.user.username)
            chatemail.delay(content, profile2.user.email)
        return redirect('chatlist')


def meetingcreate(request):
    if request.POST:
        profile1 = Profile.objects.get(user=request.user)
        profile2 = Profile.objects.get(user__id=request.POST['user'])
        content = request.POST['content']
        print(profile2)
        meeting = Meeting.objects.create(meeting=content, usercommenting=profile1, usercommentedon=profile2)
        meeting.save()
        print(request.POST['user'])
        return redirect('userpage', int(profile2.id))


###### API VIEWS

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message


class SkillLookup(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class MessagesListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chatid = self.kwargs['pk']
        userchatinstance = UserChat.objects.get(id=chatid)
        messages = Message.objects.filter(chat=userchatinstance)
        print(messages)
        return messages


class MessagesCreateView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        chat = request.data['chat']
        text = request.data['text']
        user1 = request.data['user1']
        sender = Profile.objects.get(user=User.objects.get(username=user1))
        chat = UserChat.objects.get(id=chat)
        message = Message.objects.create(chat=chat, text=text, sender=sender)
        message.save()
        return Response(status=status.HTTP_201_CREATED)


class SkillZipcode(generics.ListAPIView):
    serializer_class = SkillSerializer

    def get_queryset(self):
        skills = []
        zip = self.kwargs['zip']
        profiles = Profile.objects.filter(zipcode=zip)
        for profile in profiles:
            if profile.user != self.request.user:
                for skill in profile.skills.all():
                    print(skill)
                    skills.append(skill.id)
                    print("we")
                print(skills)
        listofskills = Skill.objects.filter(pk__in=skills)
        print(listofskills)
        return listofskills

class LearnCreateView(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        print("te")
        skill = Skill.objects.get(name=request.data['skill'])
        text = request.data['description']
        user = request.data['user']
        print(skill, text, user)
        profile = Profile.objects.get(user_id=user)
        print(profile.learn.all())
        if skill in profile.learn.all() or skill in profile.skills.all():
            pass
        else:
            learn = SkillLearn.objects.create(user=profile, skill=skill, description=text)
            learn.save()
            print(learn)
        return Response(status=status.HTTP_201_CREATED)

class KnowCreateView(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        print("te")
        skill = Skill.objects.get(skill=request.data['skill'])
        text = request.data['description']
        user = request.data['user']
        profile = Profile.objects.get(user_id=user)
        learn = SkillLearn.objects.create(user=profile, skill=skill, description=text)
        learn.save()
        return Response(status=status.HTTP_201_CREATED)