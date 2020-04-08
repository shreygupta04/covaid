import requests
import json
import secrets


response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=Oakton,3413,Waples,Glen,Court&destinations=Ashburn,23021,Olympia,Drive&key=' + secrets.API_KEY)

data = response.json()
print(data)