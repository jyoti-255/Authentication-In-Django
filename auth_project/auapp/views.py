from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from random import choice
from django.core.mail import send_mail

def urnp(request):
    if request.user.is_authenticated:
        return redirect("uhome")
    elif request.method == "POST":
        un = request.POST.get("un")
        try:
            usr = User.objects.get(username=un)
            txt = "0123456789"
            pw = ""
            for _ in range(1, 5):
                pw += choice(txt)
            usr.set_password(pw)
            usr.save()
            subject = "New Password for Kamal Classes"
            text = f"Your new password is: {pw}"
            from_email = "jyoti02056@gmail.com"
            to_email = [un]
            send_mail(subject, text, from_email, to_email)
            return redirect("ulogin")
        except User.DoesNotExist:
            msg = "Sorry, you are not registered."
            return render(request, "rnp.html", {"msg": msg})
    else:
        return render(request, "rnp.html")

def usignup(request):
    if request.user.is_authenticated:
        return redirect("uhome")
    elif request.method == "POST":
        un = request.POST.get("un")
        try:
            usr = User.objects.get(username=un)
            msg = f"{un} already registered"
            return render(request, "signup.html", {"msg": msg})
        except User.DoesNotExist:
            txt = "0123456789"
            pw = ""
            for _ in range(1, 5):
                pw += choice(txt)

            usr = User.objects.create_user(username=un, password=pw)
            usr.save()

            subject = "Welcome to Kamal Classes"
            text = f"Your password is: {pw}"
            from_email = "jyoti02056@gmail.com"
            to_email = [un]

            send_mail(subject, text, from_email, to_email)

            return render(request, "signup.html", {"msg": f"Account created for {un}. Check your email for the password."})

    return render(request, "signup.html")

def ulogin(request):
    if request.user.is_authenticated:
        return redirect("uhome")
    
    if request.method == "POST":
        un = request.POST.get("un")
        pw = request.POST.get("pw")
        usr = authenticate(username=un, password=pw)
        
        if usr is None:
            msg = "Invalid username / password"
            return render(request, "login.html", {"msg": msg})
        else:
            login(request, usr)
            return redirect("uhome")
    
    return render(request, "login.html")

def uhome(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return redirect("ulogin")

def ulogout(request):
    logout(request)
    return redirect("ulogin")

