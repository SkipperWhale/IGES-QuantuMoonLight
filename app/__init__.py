
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1/quantumknn_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "jshwifhjwieoajhf5847f5ae4eaws"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "loginPage"
login_manager.login_message_category = "info"

from app.source.model import models

# Create database if it does not exist
if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])
    with app.app_context():
        db.create_all()
else:
    with app.app_context():
        db.create_all()


from app.source.classificazioneDataset import ClassifyControl
from app.source.preprocessingDataset import PreprocessingControl
from app.source.validazioneDataset import ValidazioneControl
from app.source.gestione import GestioneControl
from app.source.utente import UtenteControl
from app.source.blog import BlogControl
from app import routes
