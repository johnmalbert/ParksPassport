# ParksPassport
This Django application built in python allows you to view information on 60 major US National Parks.
Required API Keys for use: Google Maps, National Parks Service, OpenWeatherMap

To use this application, first install Django on your local machine (More on that here... https://docs.djangoproject.com/en/3.2/howto/windows/)

If you already have Django installed, activate your virtual environment. Navigate to the directory and run 

call *ENV_NAME*\Scripts\activate 

Clone the parks passport code, and navigate to the hike_planner dir. Once there, run 

python manage.py runserver

Boom, the application will be up and running on your localhost:8000. However, the app is not fully set up yet. Register a new user (name, email, pw, etc), then type this address into the browser:

http://localhost:8000/createallparksadmin

This may take some time, it is fetching API data on all the National Parks. 

Once complete, you're good to go!
