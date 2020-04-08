import requests

API_KEY = 'AIzaSyADuVGqvUTqN-LSk8zen6PufXuJP9wHN2Y'

response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=Oakton,3413,Waples,Glen,Court&destinations=Ashburn,23021,Olympia,Drive&key=' + API_KEY)

data = response.json()