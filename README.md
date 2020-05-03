# Covaid
CovAid is a web application that connects volunteers to those in need during the COVID-19 outbreak using AI-driven intelligence. The website connects at-risk users with volunteers willing to donate necessities. Users can make requests for items to the website and volunteers can respond to those requests. These pairings are created efficiently with a machine learning algorithm that takes into account various factors such as the distance between the user and the volunteer.

## Motivation
The world we live in has changed dramatically amidst the COVID-19 outbreak. Although some of us are safe at home with the proper equipment, a large portion of the population does not have access to essentials. In analyzing the issue, we realized the immunocompromised currently had no access to essentials as they could not simply leave their houses to go to a grocery store. We decided to provide a solution to this problem by creating a website in which we could allow users to make virtual requests for items, such as toilet paper or hand sanitizer, and then enable volunteers to accept these requests to donate supplies to them. As there is no preexisting platform that allows for direct pairings between users and volunteer deliverers, we believe this is the perfect solution to help those most impacted by COVID-19.

## Getting Started
Add a Flask secret key in your venv or in a `.env` file. This will look something like `FLASK_SECRET_KEY=YOUR KEY` if it is in a `.env`, otherwise add export before the statement if it is a part of your venv.

### Running
Navigate to the directory that contains the project and run the line below in the terminal. This will launch a Flask server which will provide a local host link that displays the website.
```
python run.py
```

## Demo Video
[![demo video](https://img.youtube.com/vi/B3bwGrfTrjA/0.jpg)](https://www.youtube.com/watch?v=B3bwGrfTrjA)

## Deployment
This can be deployed on Heroku by following the steps below.
  * [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python)

## Built With
* [Flask](https://flask.palletsprojects.com/en/1.1.x/ "Flask")
* [Bootstrap](https://getbootstrap.com/ "Bootstrap")
* [Keras](https://keras.io/ "Keras")
* [Google Matrix API](https://developers.google.com/maps/documentation/distance-matrix/start "Google Matrix API")
