from django.shortcuts import render_to_response
from django.template import RequestContext
from swap.models import Skill, Profile, SkillLearn, SkillKnow
from rest_framework import generics
from rest_framework import serializers
from rest_framework import filters
from swap.forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render_to_response("home.html", context_instance=RequestContext(request))

def profile(request):
    context = {}
    profile = Profile.objects.get(user = request.user)
    context['address'] = profile.address
    context['phone'] = profile.phone
    context['know'] = profile.skills.all()
    context['learn'] = profile.learn.all()
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
                addskill = SkillLearn.objects.create(description=description, user=profile, skill=eskill)
                addskill.save()
            if skilltype == "know":
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
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
             #   profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)



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