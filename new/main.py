from flask import Flask
import os

app = Flask(__name__, template_folder='app/templates')

from app.routes import *
