from flask import Flask
import os

# initiate flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# import views
from views import *

if __name__ == '__main__':
    app.run(debug=True)
