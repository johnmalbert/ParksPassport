from django.shortcuts import render, redirect
from .models import User, Park
from django.contrib import messages
import bcrypt
import requests
import math
from datetime import datetime

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
            return redirect('/parks')
        else:
            messages.error(request, "Invalid Email and Password Combination.")
    else:
        messages.error(request, "Email given is not in the system. Please register.")
    return redirect('/userlogin')

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
        return redirect('/parks')
    return redirect('/')

def userlogin(request):
    #display login info
    return render(request, "user_login.html")

def park_by_number(request, number):
    this_park = Park.objects.get(id=number)
    lon = this_park.long
    lat = this_park.lat
    API_KEY = 'd36ad86fcc0091b23f6132b4b6cc00e7'

    # baseURL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid={API_KEY}"
    # response = requests.get(baseURL)
    # weather_data = response.json()
    weather = {}
    # curr = weather_data['current']
    # print(curr)
    # temp = math.floor(curr['temp'])
    # cond = curr['weather'][0]['description']
    # sunrise = datetime.fromtimestamp(curr['sunrise'])
    # sunset = datetime.fromtimestamp(curr['sunset'])
    # high = math.floor(weather_data['daily'][0]['temp']['max'])
    # low = math.floor(weather_data['daily'][0]['temp']['min'])
    # weather['park_temp'] = temp
    # weather['park_cond'] = cond
    # weather['sunrise'] = sunrise
    # weather['sunset'] = sunset
    # weather['max'] = high
    # weather['min'] = low

    # print(weather['park_temp'], weather['park_cond'], weather['sunrise'], weather['sunset'])
    # print(this_park.name)
    context = {
        "this_park" : this_park,
        "this_user" : User.objects.get(id = request.session['userid']),
        "weather" : weather,
    }
    return render(request, "home.html", context)

def parks(request):
    # perform hike api search
    allparks = Park.objects.all()
    context = {
        "all_parks" : allparks,
        "this_user" : User.objects.get(id=request.session['userid'])
    }
    return render(request, "parks.html", context)

def logout(request):
    del request.session['userid']
    return redirect('/userlogin')

def create_parks(request):
    if (request.session['userid']) != 1:
        return redirect('/parks')
    parks_list = ['acad', 'arch', 'badl', 'bibe', 'bisc', 'blca', 'brca', 'cany', 'care', 'cave', 'chis', 'cong', 'crla', 
    'cuva', 'deva', 'dena', 'drto', 'ever', 'gaar', 'jeff', 'glac', 'glba', 'grca', 'grte', 'grba', 'grsa', 'grsm', 'gumo', 
    'hale', 'havo', 'hosp', 'indu', 'isro', 'jotr', 'katm', 'kefj', 'kova', 'lacl', 'lavo', 'maca', 'meve', 'mora', 'neri', 'noca',
    'olym', 'pefo', 'pinn', 'redw', 'romo', 'sagu', 'kimo', 'shen', 'thro', 'viis', 'voya', 'whsa', 'wica', 'wrst', 'yell', 'yose', 'zion']
    user_str = "yell"
    api_key_nps = "GeD3b0hdw5tjKddemD7MkjHLvL9CLBJei3EJRgnf"
    baseURL_nps = f"https://developer.nps.gov/api/v1/parks?parkCode={user_str}&api_key={api_key_nps}"
    resp = requests.get(baseURL_nps)
    park_data = resp.json()
    for i in parks_list:
        user_str = i
        api_key_nps = "GeD3b0hdw5tjKddemD7MkjHLvL9CLBJei3EJRgnf"
        baseURL_nps = f"https://developer.nps.gov/api/v1/parks?parkCode={user_str}&api_key={api_key_nps}"
        resp = requests.get(baseURL_nps)
        park_data = resp.json()
        Park.objects.create(
            name = park_data['data'][0]['fullName'],
            url = park_data['data'][0]['url'],
            desc = park_data['data'][0]['description'],
            long = park_data['data'][0]['longitude'],
            lat = park_data['data'][0]['latitude'],
            img_url = park_data['data'][0]['images'][0]['url'],
            parkCode = user_str
        )
    print("Success!")
    return redirect('/parks')