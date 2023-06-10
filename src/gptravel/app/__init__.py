from flask import Flask

app = Flask(__name__)

from src.gptravel.app import routes