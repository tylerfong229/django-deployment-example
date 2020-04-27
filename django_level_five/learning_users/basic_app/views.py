from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# For log in
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

def register(request):
    # assume at first not registered
    registered = False

    # if its a post request
    if request.method == 'POST':

        # Grab the form inputs
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        # use built in validate function to check theyre both valid
        if user_form.is_valid() and profile_form.is_valid():

            # grab the stuff from the userform
            user = user_form.save()
            user.set_password(user.password) #Hashing the password
            user.save()

            # grab profile_form information
            profile = profile_form.save(commit = False)
            profile.user = user # sets up the 1:1 relationship

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            # note that they are now registered
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # authoenticates user in one line!
        user = authenticate(username = username, password = password)

        if user:
            # if an actual user and active, redirect to index page
            if user.is_active:
                print('user is active and authentic')
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print('SOMEONE TRIED TO LOG IN AND FAILED')
            print('Username: {} and password {}'.format(username, password))
            return HttpResponse('invalid login details supplied!')
    else:
        return render(request, 'basic_app/login.html', {})

# Decorator function to ensure user is logged in.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
