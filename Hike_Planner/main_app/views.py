from django.shortcuts import render, redirect
from .models import User, Park
from django.contrib import messages
import bcrypt
import requests
import math
from datetime import datetime
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request, "login.html")

def registerdata(request):
    context = {
        "message" : "Users can customize app experience, including directions and search preferences. We will never email you. Hint: Use a fake email!"
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
            request.session['allparks'] = True
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

    weather = {}
    baseURL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid={API_KEY}"
    response = requests.get(baseURL)
    weather_data = response.json()
    curr = weather_data['current']
    print(curr)
    temp = math.floor(curr['temp'])
    cond = curr['weather'][0]['description']
    sunrise = datetime.fromtimestamp(curr['sunrise'])
    sunset = datetime.fromtimestamp(curr['sunset'])
    high = math.floor(weather_data['daily'][0]['temp']['max'])
    low = math.floor(weather_data['daily'][0]['temp']['min'])
    weather['park_temp'] = temp
    weather['park_cond'] = cond
    weather['sunrise'] = sunrise
    weather['sunset'] = sunset
    weather['max'] = high
    weather['min'] = low

    print(weather['park_temp'], weather['park_cond'], weather['sunrise'], weather['sunset'])
    print(this_park.name)
    context = {
        "this_park" : this_park,
        "this_user" : User.objects.get(id = request.session['userid']),
        "weather" : weather,
    }
    return render(request, "home.html", context)

def parks(request):
    # perform hike api search
    first_parks = []
    for i in range(1,9):
        new_park = Park.objects.get(id=i)
        first_parks.append(new_park)
    # allparks = Park.objects.all()
    request.session['allparks'] = True
    context = {
        "all_parks" : first_parks,
        "this_user" : User.objects.get(id=request.session['userid'])
    }
    return render(request, "parks.html", context)

def allparks(request):
    allparks = Park.objects.all()
    request.session['allparks'] = False
    context = {
        "all_parks" : allparks,
        "this_user" : User.objects.get(id=request.session['userid'])
    }
    return render(request, "parks.html", context)

def logout(request):
    del request.session['userid']
    return redirect('/userlogin')

def account(request):
    context = {
        "this_user" : User.objects.get(id=request.session['userid'])
    }
    return render(request, "my_account.html", context)

def update_account(request):
    print("update the account.")
    return redirect('/account')

def visit_park(request, number):
    #get park by #
    this_park = Park.objects.get(id=number)
    #get user by #
    this_user = User.objects.get(id=request.session['userid'])
    this_park.visits.add(this_user)
    print(f"Park {this_park.id} was visited by User # {this_user.id}")
    return redirect('/parks/user/visited')

def leaders(request):
    # list all the users by leader, then list the current user if not listed
    all_users = User.objects.annotate(cc=Count('visited_parks')).order_by('-cc')
    context = {
        "all_users" : all_users,
        "this_user" : User.objects.get(id=request.session['userid']),
    }
    return render(request, "all_users.html", context)


def visited_parks(request):
    context = {
        "this_user" : User.objects.get(id=request.session['userid']),
    }
    return render(request, "visited_parks.html", context)

def user_passport(request, number):
    this_user = User.objects.get(id=request.session['userid'])
    current_user = User.objects.get(id=number)
    context = {
        "this_user" : this_user,
        "passport_user" : current_user
    }
    return render(request, "user_passport.html", context)


def create_parks(request):
    print("Creating all the parks.")
    if (request.session['userid']) != 1:
        return redirect('/parks')
    parks_list = ['acad', 'arch', 'badl', 'bibe', 'bisc', 'blca', 'brca', 'cany', 'care', 'cave', 'chis', 'cong', 'crla', 
    'cuva', 'deva', 'dena', 'drto', 'ever', 'gaar', 'glac', 'glba', 'grca', 'grte', 'grba', 'grsa', 'grsm', 'gumo', 
    'hale', 'havo', 'hosp', 'indu', 'isro', 'jotr', 'katm', 'kefj', 'kova', 'lacl', 'lavo', 'maca', 'meve', 'mora', 'neri', 'noca',
    'olym', 'pefo', 'pinn', 'redw', 'romo', 'sagu', 'seki', 'shen', 'thro', 'viis', 'voya', 'whsa', 'wica', 'wrst', 'yell', 'yose', 'zion']
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
        parkname = park_data['data'][0]['fullName']
        parkname = parkname.replace("&#257;", "a")
        parkname = parkname.replace("&", "and")
        try:
            img_url2 = park_data['data'][0]['images'][1]['url']
            img2_desc = park_data['data'][0]['images'][1]['title']
        except:
            img_url2 = park_data['data'][0]['images'][0]['url']
            img2_desc = park_data['data'][0]['fullName']
        try:
            img_url3 = park_data['data'][0]['images'][2]['url']
            img3_desc = park_data['data'][0]['images'][2]['title']
        except: 
            img_url3 = park_data['data'][0]['images'][0]['url']
            img3_desc = park_data['data'][0]['fullName']
        Park.objects.create(
            name = parkname,
            url = park_data['data'][0]['url'],
            desc = park_data['data'][0]['description'],
            long = park_data['data'][0]['longitude'],
            lat = park_data['data'][0]['latitude'],
            img_url = park_data['data'][0]['images'][0]['url'],
            img_url2 = img_url2,
            img_url3 = img_url3,
            img1_desc = park_data['data'][0]['images'][0]['title'],
            img2_desc = img2_desc,
            img3_desc = img3_desc,
            parkCode = user_str
        )
    # Fix Haleakala name   
    print("Success!")
    return redirect('/parks')