from flask import Flask
from app.config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

from app import routes
