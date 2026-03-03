from django.shortcuts import render, redirect
from .models import Student
from .forms import LoginForm, UserProfileForm

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if Student.objects.filter(username=username, password=password).exists():
                return redirect("dashboard")
            else:
                return render(request, "accounts/login.html",
                              {"form": form, "error": "Invalid username/password"})

    return render(request, "accounts/login.html", {"form": form})


def dashboard(request):
    return render(request, "accounts/dashboard.html")


def user_form(request):
    form = UserProfileForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("dashboard")

    return render(request, "accounts/user_form.html", {"form": form})