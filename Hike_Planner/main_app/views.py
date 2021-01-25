from django.shortcuts import render, redirect

# Create your views here.
def login(request):
    return render(request, "login.html")

def homepage(request):
    return render(request, "home.html")

def register(request):
    # Perform register process
    return redirect('/home')

def userlogin(request):
    #display login info
    return render(request, "user_login.html")

def hike_finder(request):
    # perform hike api search
    return render(request, "hike_finder.html")