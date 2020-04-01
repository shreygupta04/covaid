from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f21ee4e68cf4363ef42235910dcb041a'

from covaid import routes