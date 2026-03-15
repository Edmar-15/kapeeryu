from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, AccountCompletion
from .models import UserProfile

# Decorators here.

def anonymous_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def verified_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = request.user.userprofile_set.first()
            if not profile or not profile.is_verified:
                return redirect('verification')
        return view_func(request, *args, **kwargs)
    return wrapper

# Create your views here.
@anonymous_required
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('verification')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form':form})

@anonymous_required
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            profile = user.userprofile_set.first()
            if not profile or not profile.is_verified:
                return redirect('verification')
            return redirect('home')
        
    return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@verified_required
def home(request):
    return render(request, 'home.html')

@login_required
def account_completion(request):
    if request.method == 'POST':
        form = AccountCompletion(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AccountCompletion()

    return render(request, 'account_completion.html', {'form':form})