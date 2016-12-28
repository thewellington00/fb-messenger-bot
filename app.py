import os
import sys
import json

import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# initiate flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# models
from models import *

# views
from views import *


if __name__ == '__main__':
    app.run(debug=True)
