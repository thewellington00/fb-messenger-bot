from flask import Flask
import os

# initiate flask app
app = Flask(__name__)

# import views
from views import *

if __name__ == '__main__':
    app.run(debug=True)
