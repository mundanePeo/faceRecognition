

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

model = SQLAlchemy() 


def init_ext(app):
    # SQL
    model.init_app(app)
    
    
    

    
# def init_fr_model():
