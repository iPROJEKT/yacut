from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, session_options={"expire_on_commit": False})
migrate = Migrate(app, db)


from . import views, models, api_views, error_handlers, forms
