from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('flaskr.config')

db = SQLAlchemy(app)


from flaskr.models.database import Ingredient, Step, Recipe_ingredient, Recipe_step, Recipe, User

import flaskr.main
