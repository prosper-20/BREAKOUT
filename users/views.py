import imp
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been successfully created for {username}. Kindly login with your credentials below ')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
            


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, "You are logged in")
            return redirect('/')
        else:
            messages.error(request, "Credentials not valid")
            return redirect("login")
    #You changed from login.htnl to form-login
    return render(request, 'users/login_2.html')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]


        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Oops, the username entered already exixts")
                return redirect("register")
            elif User.objects.filter(email=email).exits():
                messages.info(request, "Email address already taken")
            else:
                user = User.objects.create_user(username=username,
                email=email, password=password)
                user.save()
                messages.info(request, "Hi {username}, your account creation was successful! Kindly login below")
                return redirect("login")
        else:
            messages.error(request, "Both passwords didn't match")
            return redirect("register")
    
    return render(request, "users/regitser_2.html")