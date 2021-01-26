from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt
import requests
import math

# Create your views here.
def index(request):
    return render(request, "login.html")

def registerdata(request):
    context = {
        "message" : "Users can customize app experience, including directions and search preferences. We will never email you."
    }
    return render(request, "login.html", context)

def login(request):
    this_user = User.objects.filter(email=request.POST['email'].lower())
    if this_user:
        print("user exists with email ", request.POST['email'])
        logged_user = this_user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            # if we get True after checking the password, we may put the user id in session
            request.session['userid'] = logged_user.id
            # never render on a post, always redirect!
            return redirect('/home')
        else:
            messages.error(request, "Invalid Email and Password Combination.")
    else:
        messages.error(request, "Email given is not in the system. Please register.")
    return redirect('/userlogin')

def homepage(request):
    #get park info
    user_str = "zion"
    api_key_nps = "GeD3b0hdw5tjKddemD7MkjHLvL9CLBJei3EJRgnf"
    baseURL_nps = f"https://developer.nps.gov/api/v1/parks?parkCode={user_str}&api_key={api_key_nps}"
    resp = requests.get(baseURL_nps)
    park_data = resp.json()
    print(park_data['data'][0]['url'])
    park_name = park_data['data'][0]['fullName']
    park_url = park_data['data'][0]['url']
    park_desc = park_data['data'][0]['description']
    park_long = park_data['data'][0]['longitude']
    park_lat = park_data['data'][0]['latitude']
    img_url = park_data['data'][0]['image'][0]

    lon =  park_long
    lat =  park_lat
    API_KEY = 'd36ad86fcc0091b23f6132b4b6cc00e7'

    # baseURL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid={API_KEY}"
    # print(baseURL)
    # response = requests.get(baseURL)
    # weather_data = response.json()
    # curr = weather_data['current']
    # temp = math.floor(curr['temp'])
    # cond = curr['weather'][0]['description']
    context = {
        "this_user" : User.objects.get(id=request.session['userid']),
        "park_name" : park_name,
        "park_url" : park_url,
        "park_desc" : park_desc,
        "park_long" : park_long,
        "park_lat" : park_lat,
        "park_img" : park_img
        # "park_temp" : temp,
        # "park_cond" : cond
    }
    return render(request, "home.html", context)

def register(request):
    # Perform register process
    print(request.POST)
    errors = User.objects.UserValidation(request.POST)
    request.session['login'] = False
    if len(errors) > 0:
        print(errors)
        print("Cant create one yet. ")
        for msg in errors.values():
            messages.error(request, msg)
    else:
        #create a user login registration
        print("Go ahead and make a user.")
        password = request.POST['password']
        pw_encrypted = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_encrypted)
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'].lower(),
            zipcode = request.POST['zipcode'],
            password = pw_encrypted
        )
        print(User.objects.last())
        print('successful user creation')
        request.session['userid'] = User.objects.last().id
        print(request.session['userid'])
        return redirect('/home')
    return redirect('/')

def userlogin(request):
    #display login info
    return render(request, "user_login.html")

def hike_finder(request):
    # perform hike api search
    return render(request, "hike_finder.html")

def logout(request):
    del request.session['userid']
    return redirect('/userlogin')