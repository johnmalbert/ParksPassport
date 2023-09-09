from django.shortcuts import render, redirect
from .models import User, Park, Rating
from django.contrib import messages
from .forms import ParkSearchForm
import bcrypt
import requests
import math
from datetime import datetime
from django.db.models import Count
import random
import os
import openai
import config

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
            request.session['parksGame'] = 0
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
        request.session['parksGame'] = 0
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
    weather = {}
    baseURL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid={config.API_KEY}"
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
    icon = curr['weather'][0]['icon']
    weather['icon'] = f"http://openweathermap.org/img/wn/{icon}@2x.png"

    # make call to OpenAI
    openai.api_key = "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"

    # # Call OpenAI's API
    # reasons_to_visit = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=f"You are a park ranger. Give the top 5 hikes and the distances in this park: {this_park.name} I want the reasons in a numbered list. \n",
    #     temperature=0.7,
    #     max_tokens=150,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0
    # )
    # print(reasons_to_visit)
    # print(reasons_to_visit.choices[0].text)
    # this_park.desc = reasons_to_visit.choices[0].text
    try:
        this_user = User.objects.get(id = request.session['userid'])
    except:
        context = {
            "this_park" : this_park,
            "weather" : weather,
            "maps_key" : config.maps_key
        }
        return render(request, "home.html", context)
    context = {
        "this_park" : this_park,
        "this_user" : User.objects.get(id = request.session['userid']),
        "weather" : weather,
        "maps_key" : config.maps_key
    }
    return render(request, "home.html", context)

def parks(request):
    # perform hike api search
    try:
        request.session['userid']
    except: 
        return redirect('/parks/guest')
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
    all_parks = Park.objects.all()

    # Handle search
    search_query = request.GET.get('search_query')
    if search_query:
        all_parks = all_parks.filter(name__icontains=search_query)

    try:
        request.session['userid']
    except: 
        return redirect('/parks/allparks/guest')
    request.session['allparks'] = False
    park_codes = { 
        "acad": "acad.png",
        "arch": "arch.png",
        "badl": "badl.png",
        "bisc": "bisc.png",
        "blca": "blca.png",
        "brca": "brca.png",
        "cany": "cany.png",
        "cave": "cave.png",
        "chis": "chis.png",
        "cong": "cong.png",
        "crla": "crla.png",
        "cuva": "cuva.png",
        "dena": "dena.png",
        "deva": "deva.png",
        "drto": "drto.png",
        "ever": "ever.png",
        "gaar": "gaar.png",
        "glac": "glac.png",
        "glba": "glba.png",
        "grba": "grba.png",
        "grca": "grca.png",
        "gumo": "gumo.png",
        "hale": "hale.png",
        "havo": "havo.png",
        "hosp": "hosp.png",
        "isro": "isro.png",
        "jotr": "jotr.png",
        "katm": "katm.png",
        "kefj": "kefj.png",
        "kica": "kica.png",
        "kova": "kova.png",
        "lavo": "lavo.png",
        "maca": "maca.png",
        "meve": "meve.png",
        "mora": "mora.png",
        "noca": "noca.png",
        "olym": "olym.png",
        "pefo": "pefo.png",
        "pinn": "pinn.png",
        "redw": "redw.png",
        "romo": "romo.png",
        "sagu": "sagu.png",
        "seki": "seki.png",
        "shen": "shen.png",
        "thro": "thro.png",
        "viis": "viis.png",
        "voja": "voja.png",
        "voyu": "voyu.png",
        "wica": "wica.png",
        "wrst": "wrst.png",
        "yell": "yell.png",
        "yose": "yose.png",
        "zion": "zion.png",
    }
    context = {
        "all_parks": all_parks,
        "this_user": User.objects.get(id=request.session['userid']),
        "park_codes": park_codes,
        # 'search_form': ParkSearchForm()
    }
    # return render(request, "parks.html", context)
    return render(request, 'parks.html', context)

def logout(request):
    del request.session['userid']
    return redirect('/userlogin')

def account(request):
    print(request.POST.get('input'))
    if request.method == 'POST':
        user_input = request.POST.get('input')
        headers = {'Authorization': '<enter openai key>'}
        data = {
            'prompt': user_input,
            'temperature': 0.5,
            'max_tokens': 60,
        }
        print(headers)
        # response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, json=data)
    #     if response.status_code == 200:
    #         chat_response = response.json()['choices'][0]['text']
    #     else:
    #         print(response)
    #         chat_response = "I'm sorry, I couldn't understand you. Can you please rephrase?"
    # else:
    #     chat_response = "Hello! How can I help you today?"
        
    try:
        request.session['userid']
    except: 
        return redirect('/')
    context = {
        "this_user" : User.objects.get(id=request.session['userid']),
        'chat_response': chat_response
    }
    print(chat_response)
    return render(request, "my_account.html", context)



def update_account(request):
    print("update the account.")
    try:
        request.session['userid']
    except: 
        return redirect('/')
    return redirect('/account')

def visit_park(request, number):
    #get park by #
    this_park = Park.objects.get(id=number)
    #get user by #
    try:
        request.session['userid']
    except: 
        return redirect('/')
    this_user = User.objects.get(id=request.session['userid'])
    this_park.visits.add(this_user)
    # add rating for the new park
    new_rating = Rating.objects.create(
        parkId = number,
        parkRating = 5,
        owner = this_user
    )
    #reroute depending on where user came from
    return redirect('/parks/allparks')

def visit_park_from_page(request, number):
    #get park by #
    this_park = Park.objects.get(id=number)
    #get user by #
    try:
        request.session['userid']
    except: 
        return redirect('/')
    this_user = User.objects.get(id=request.session['userid'])
    this_park.visits.add(this_user)
    # add a new rating for the added park.
    new_rating = Rating.objects.create(
        parkId = number,
        parkRating = 0,
        owner = this_user
    )
    #reroute depending on where user came from
    return redirect(f'/parks/{number}')

def remove_visit(request, number):
    this_park = Park.objects.get(id=number)
    this_user = User.objects.get(id=request.session['userid'])
    this_park.visits.remove(this_user)
    return redirect('/parks/allparks')

def remove_visit_from_page(request, number):
    this_park = Park.objects.get(id=number)
    this_user = User.objects.get(id=request.session['userid'])
    this_park.visits.remove(this_user)
    return redirect(f'/parks/{number}')

def leaders(request):
    # list all the users by leader, then list the current user if not listed
    all_users = User.objects.annotate(cc=Count('visited_parks')).order_by('-cc')
    try:
        request.session['userid']
    except:
        context = {
            "all_users" : all_users,
        }
        return render(request, "all_users.html", context)
    context = {
        "all_users" : all_users,
        "this_user" : User.objects.get(id=request.session['userid']),
    }
    return render(request, "all_users.html", context)


def visited_parks(request):
    try:
        request.session['userid']
    except: 
        return redirect('/')
    context = {
        "this_user" : User.objects.get(id=request.session['userid']),
    }
    return render(request, "visited_parks.html", context)

def user_passport(request, number):
    try:
        request.session['userid']
    except: 
        current_user = User.objects.get(id=number)
        context = {
            "passport_user" : current_user
        }
        return render(request, "user_passport.html", context)
    this_user = User.objects.get(id=request.session['userid'])
    current_user = User.objects.get(id=number)
    context = {
        "this_user" : this_user,
        "passport_user" : current_user
    }
    return render(request, "user_passport.html", context)

def random_park(request):
    #create a random number, redirect to that park's page
    rand = random.randrange(1,len(Park.objects.all()))
    return redirect(f"/parks/{rand}")

def parks_game(request):
    try:
        request.session['userid']
    except: 
        return redirect('/')
    this_user = User.objects.get(id=request.session['userid'])
    rand = random.randrange(0,len(this_user.visited_parks.all()))
    rand2 = random.randrange(0,len(this_user.visited_parks.all()))
    while(rand == rand2):
        rand2 = random.randrange(0,len(this_user.visited_parks.all()))
    # get list of current user's passport
    # find two random parks
    parks_list = []
    for park in this_user.visited_parks.all():
        parks_list.append(park)
    park1 = parks_list[rand]
    park2 = parks_list[rand2]
    context = {
        "this_user" : this_user,
        "park1" : park1,
        "park2" : park2
    }
    return render(request, "parks_game.html", context)

def rank_park(request, winner, loser):
    if request.session['parksGame'] > 10:
        return redirect('/parks/ranked')
    current_user = User.objects.get(id=request.session['userid'])
    park_rating = Rating.objects.get(parkId = winner, owner = current_user)
    park_rating_loser = Rating.objects.get(parkId = loser, owner = current_user)
    # print(f"Park {winner} is rated {park_rating.parkRating}")
    park_rating.parkRating = park_rating.parkRating + 2
    park_rating_loser.parkRating = park_rating_loser.parkRating - 1
    print(f"{park_rating.parkId} is rated {park_rating.parkRating}")
    park_rating.save()
    request.session['parksGame'] += 1
    print(request.session['parksGame'])
    # assign 5 pts to winner
    # take away 1 pt from loser
    return redirect('/parks/game')

def display_ranked_parks(request):
    try:
        request.session['userid']
    except: 
        return redirect('/')
    this_user = User.objects.get(id=request.session['userid'])
    request.session['parksGame'] = 0
    # rank all the parks in order
    park_ratings = Rating.objects.filter(owner = this_user).order_by("-parkRating")
    list = []
    for rating in park_ratings:
        list.append(Park.objects.get(id=rating.parkId))
    for park in park_ratings:
        print(f"{park.parkId} is rated {park.parkRating}")
    # get the user's rankings:
    context = {
        "this_user" : this_user,
        "parks_in_order" : list,
    }
    return render(request, "ranked.html", context)

def create_parks(request):
    print("Creating all the parks.")
    if (request.session['userid']) != 1:
        return redirect('/parks')
    parks_list = ['acad', 'arch', 'badl', 'bibe', 'bisc', 'blca', 'brca', 'cany', 'care', 'cave', 'chis', 'cong', 'crla', 
    'cuva', 'deva', 'dena', 'drto', 'ever', 'gaar', 'glac', 'glba', 'grca', 'grte', 'grba', 'grsa', 'grsm', 'gumo', 
    'hale', 'havo', 'hosp', 'indu', 'isro', 'jotr', 'katm', 'kefj', 'kova', 'lacl', 'lavo', 'maca', 'meve', 'mora', 'neri', 'noca',
    'olym', 'pefo', 'pinn', 'redw', 'romo', 'sagu', 'seki', 'shen', 'thro', 'viis', 'voya', 'whsa', 'wica', 'wrst', 'yell', 'yose', 'zion']
    user_str = "yell"
    
    baseURL_nps = f"https://developer.nps.gov/api/v1/parks?parkCode={user_str}&api_key={config.api_key_nps}"
    resp = requests.get(baseURL_nps)
    park_data = resp.json()
    for i in parks_list:
        user_str = i
        api_key_nps = "GeD3b0hdw5tjKddemD7MkjHLvL9CLBJei3EJRgnf"
        baseURL_nps = f"https://developer.nps.gov/api/v1/parks?parkCode={user_str}&api_key={api_key_nps}"
        resp = requests.get(baseURL_nps)
        park_data = resp.json()
        parkname = park_data['data'][0]['fullName']
        # parkname = parkname.replace("&#257;", "a")
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
        try:
            img_url4 = park_data['data'][0]['images'][3]['url']
            img4_desc = park_data['data'][0]['images'][3]['title']
        except: 
            img_url4 = park_data['data'][0]['images'][0]['url']
            img4_desc = park_data['data'][0]['fullName']
        Park.objects.create(
            name = parkname,
            url = park_data['data'][0]['url'],
            desc = park_data['data'][0]['description'],
            long = park_data['data'][0]['longitude'],
            lat = park_data['data'][0]['latitude'],
            img_url = park_data['data'][0]['images'][0]['url'],
            img_url2 = img_url2,
            img_url3 = img_url3,
            img_url4 = img_url4,
            img1_desc = park_data['data'][0]['images'][0]['title'],
            img2_desc = img2_desc,
            img3_desc = img3_desc,
            img4_desc = img4_desc,
            parkCode = user_str
        )
    # Fix Haleakala name   
    print("Success!")
    request.session['created'] = True
    return redirect('/parks')

#Guest accessable pages: Parks, park_by_number, allparks, leaders, random_park\
def park_by_number_guest(request, number):
    try:
        request.session['userid']
    except: 
        return redirect('/')
    this_park = Park.objects.get(id=number)
    lon = this_park.long
    lat = this_park.lat
    weather = {}
    baseURL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid={config.API_KEY}"
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
    icon = curr['weather'][0]['icon']
    weather['icon'] = f"http://openweathermap.org/img/wn/{icon}@2x.png"
    context = {
        "this_park" : this_park,
        "this_user" : User.objects.get(id = request.session['userid']),
        "weather" : weather,
        "maps_key" : config.maps_key
    }
    return render(request, "home.html", context)

def parks_guest(request):
    first_parks = []
    for i in range(1,9):
        new_park = Park.objects.get(id=i)
        first_parks.append(new_park)
    # allparks = Park.objects.all()
    request.session['allparks'] = True
    context = {
        "all_parks" : first_parks
    }
    return render(request, "parks.html", context)

def allparks_guest(request):
    allparks = Park.objects.all()
    request.session['allparks'] = False
    context = {
        "all_parks" : allparks,
    }
    return render(request, "parks.html", context)

def admin(request):
    try:
        request.session['userid']
    except: 
        return redirect('/')
    if (request.session['userid']) != 1:
        return redirect('/parks')
    all_users = User.objects.annotate(cc=Count('visited_parks')).order_by('-cc')
    context = {
        "all_users" : all_users,
        "this_user" : User.objects.get(id=request.session['userid']),
    }
    return render(request, "admin.html", context)

def delete_user(request, user_id):
    print(User.objects.get(id=user_id))
    if (request.session['userid']) != 1:
        return redirect('/parks')
    user_to_del = User.objects.get(id=user_id)
    user_to_del.delete()
    return redirect("/admin")

park_codes = {
    "acad": "acad.png",
    "arch": "arch.png",
    "badl": "badl.png",
    "bisc": "bisc.png",
    "blca": "blca.png",
    "brca": "brca.png",
    "cany": "cany.png",
    "cave": "cave.png",
    "chis": "chis.png",
    "cong": "cong.png",
    "crla": "crla.png",
    "cuva": "cuva.png",
    "dena": "dena.png",
    "deva": "deva.png",
    "drto": "drto.png",
    "ever": "ever.png",
    "gaar": "gaar.png",
    "glac": "glac.png",
    "glba": "glba.png",
    "grba": "grba.png",
    "grca": "grca.png",
    "gumo": "gumo.png",
    "hale": "hale.png",
    "havo": "havo.png",
    "hosp": "hosp.png",
    "isro": "isro.png",
    "jotr": "jotr.png",
    "katm": "katm.png",
    "kefj": "kefj.png",
    "kica": "kica.png",
    "kova": "kova.png",
    "lavo": "lavo.png",
    "maca": "maca.png",
    "meve": "meve.png",
    "mora": "mora.png",
    "noca": "noca.png",
    "olym": "olym.png",
    "pefo": "pefo.png",
    "pinn": "pinn.png",
    "redw": "redw.png",
    "romo": "romo.png",
    "sagu": "sagu.png",
    "seki": "seki.png",
    "shen": "shen.png",
    "thro": "thro.png",
    "viis": "viis.png",
    "voja": "voja.png",
    "voyu": "voyu.png",
    "wica": "wica.png",
    "wrst": "wrst.png",
    "yell": "yell.png",
    "yose": "yose.png",
    "zion": "zion.png",
}
