from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import DeleteView, DetailView, ListView, CreateView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from swap.models import Skill, Profile, SkillLearn, SkillKnow, UserChat, Message, Meeting
from rest_framework import generics
from rest_framework import serializers
from rest_framework import filters
from swap.forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from rest_framework import authentication, permissions
import requests
from rest_framework import status
from django.db.models import Q


def home(request):
    return render_to_response("home.html", context_instance=RequestContext(request))


@login_required(redirect_field_name='login')
def profile(request):
    context = {}
    if request.POST:
        people = []
        distancemax = int(request.POST['distance'])
        profiles = Profile.objects.all()
        currentuser = Profile.objects.get(user=request.user)
        streetad = currentuser.street.strip().replace(' ', '+')
        print(streetad)
        API_KEY = 'AIzaSyCLIdr-9-bc_jnnH4tfIfIPCmAhhfGkQg8'
        currentuserdata = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + str(
            currentuser.streetnumber) + streetad + ',' + currentuser.city + ',' + currentuser.state + '&key=' + API_KEY)
        currentusercords = str(currentuserdata.json()['results'][0]['geometry']['location']['lat']) + ',' + str(
            currentuserdata.json()['results'][0]['geometry']['location']['lng'])
        for profile in profiles:
            if profile != currentuser:
                streetad = profile.street.strip().replace(' ', '+')
                profiledata = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + str(
                profile.streetnumber) + streetad + ',' + profile.city + ',' + profile.state + '&key=' + API_KEY)
                print(profile, profiledata.content)
                profilecords = str(profiledata.json()['results'][0]['geometry']['location']['lat']) + ',' + str(
                profiledata.json()['results'][0]['geometry']['location']['lng'])
                print(profilecords)
                disdata = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?origins='+currentusercords+'&destinations='+profilecords+'&key='+API_KEY)
                distance= disdata.json()['rows'][0]['elements'][0]['distance']['text']
                miles = miles = 0.62137 * int(''.join(x for x in distance if x.isdigit()))
                print(miles)
                if miles <= distancemax:
                    print(profile.skills.all())
                    people.append((profile, profile.skills.all()))
        context['people'] = people
    know = []
    learn = []
    addedsimskill = []
    exact = []
    smatch = []
    simmatch = []
    profile = Profile.objects.get(user=request.user)
    context['address'] = '{} {}, {} , {} '.format(profile.streetnumber, profile.street, profile.city, profile.state)
    context['phone'] = profile.phone
    knowall = profile.skills.all()
    learnall = profile.learn.all()
    for item in knowall:
        know.append(SkillKnow.objects.get(user=profile, skill=item))
    for ite in learnall:
        add = False
        learn.append(SkillLearn.objects.get(user=profile, skill=ite))
        match = Profile.objects.filter(skills__in=[ite])
        skillsvalue = Profile.objects.all().values_list('skills__name')
        for item in skillsvalue:
            skillname = str(item[0])
            mat = skillname.find(ite.name)
            if mat != -1:
                skil = Skill.objects.get(name=item[0])
                simmatch = Profile.objects.filter(skills__in=[skil])
                add = True
                if len(simmatch) and not skillname == ite.name and skillname != 'None' and add:
                    if not skillname in addedsimskill:
                        addedsimskill.append(skillname)
                        smatch.append((ite, simmatch, skillname))
        if len(match):
            exact.append((ite, match))
    context['exact'] = exact
    context['learn'] = learn
    context['know'] = know
    context['similiar'] = smatch

    return render_to_response("profile.html", context, context_instance=RequestContext(request))


@login_required(redirect_field_name='login')
def add_skill(request):
    context = {}
    print(request.user)
    profile = Profile.objects.get(user=request.user)
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
        profile = kwargs['object']
        reviews = Meeting.objects.filter(usercommentedon=profile)
        know = context['profile'].skills.all()
        learn = context['profile'].learn.all()
        for skill in know:
            knowall.append((skill.name, SkillKnow.objects.get(user=context['profile'], skill=skill)))
        for skill in learn:
            learnall.append((skill.name, SkillLearn.objects.get(user=context['profile'], skill=skill)))
        context['review'] = reviews
        context['know'] = knowall
        context['learn'] = learnall
        print(context)
        return context

class ChatListView(ListView):
    model = UserChat
    #profile = Profile.objects.get(user=request.user)
    #queryset = UserChat.objects.filter(Q(user1=request.user)|Q(user2=request.user))
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        print("hey")
        context = super().get_context_data(**kwargs)
        context['token'] = Token.objects.get(user=self.request.user)
        return context


def userchatview(request):
    if request.POST:
        profile1 = Profile.objects.get(user=request.user)
        profile2 = Profile.objects.get(user__username=request.POST['user2'])
        print(profile1, profile2)
        chat = UserChat.objects.create(user1=profile1, user2=profile2)
        return redirect('chatlist')

def meetingcreate(request):
    if request.POST:
        profile1 = Profile.objects.get(user=request.user)
        profile2 = Profile.objects.get(user__id=request.POST['user'])
        content = request.POST['content']
        meeting = Meeting.objects.create(meeting=content, usercommenting=profile1, usercommentedon=profile2)
        meeting.save()
        return redirect('userpage', int(request.POST['user']) )


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
        # field = ['chat', 'user1', 'user2', 'text']


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

class MessagesCreateView(generics.CreateAPIView):
    model = Message
    print("makin it")
    serializer_class = MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)