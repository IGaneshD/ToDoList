import sys
from django.shortcuts import render, HttpResponse, redirect
from .forms import UserSignInForm, CustomUserCreationForm, onboardForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

# Create your views here.

@login_required(login_url='signin')
def profile_setup_view(request):
    if request.user:
        user = request.user
        profile = Profile.objects.get(profile_owner = user)
        if profile.onboarding_done:
            return redirect('taskboard')
    
    form = onboardForm()
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(profile_owner = user)
        profile.country = request.POST['country']
        profile.onboarding_done = True
        profile.save()
        return redirect('taskboard')
    return render(request, 'users/user-onboarding.html', context={'form':form})






@login_required(login_url='signin')
def profile_view(request):

    return render(request, 'users/user-profile.html', context={'name':'Ganesh'})









def signUp_User(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Account Created Successfully")
            login(request, user)
            return redirect('onboard')
        

    return render(request, 'users/user-create.html', context={'form':form})



def signIn_User(request):

    if request.user.is_authenticated:
        return redirect('taskboard')
    
    # HACK: Method 1
    form = UserSignInForm()
    if request.method == 'POST':
        form = UserSignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request, user)
                return redirect('taskboard')
            else:
                messages.error(request, "Username or Password is Incorrect")
            
    return render(request, 'users/user-login.html', context={'form':form})


    # HACK: Method 2 without using django forms
    # username = None
    # if request.method == "POST":
    #     username = request.POST['username']
    #     password = request.POST['password']

    #     user = authenticate(username=username, password=password)
    #     if user:
    #         login(request, user)

    # return render(request, 'users/user-login.html', context={'username':username})

    # HACK: method 3 with django Authentication Form

    # form = AuthenticationForm()
    # if request.method == "POST":
    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         user = form.get_user()
    #         login(request, user)
    #         return redirect('taskboard')
        
    # return render(request, 'users/user-login.html', context={'form':form})



def signout_user(request):
    logout(request)
    return redirect('signin')






from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator

# def send_verification_email(user):
#     token = default_token_generator.make_token(user)
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     verification_link = f"http://yourwebsite.com/verify-email/{uid}/{token}/"
    
#     subject = 'Verify your email address'
#     message = render_to_string('verification_email.html', {'verification_link': verification_link})
#     user_email = user.email
#     send_mail(subject, message, 'from@example.com', [user_email])

# def verify_email(request, uidb64, token):
#     try:
#         uid = force_bytes(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.email_verified = True
#         user.save()
#         return HttpResponse('Your email has been verified successfully!')
#     else:
#         return HttpResponse('Invalid verification link!')
