from flask import Flask  
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__, template_folder='templates')
cors = CORS(app, resources={r"*": {"origins": "*"}})

app.secret_key= 'xxx'

app.config.from_object(Config)
db = SQLAlchemy(app)
jwt = JWTManager(app)




from app.models import userModel, tesModel
from app import routes