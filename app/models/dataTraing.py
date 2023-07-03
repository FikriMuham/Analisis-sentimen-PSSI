from app import db

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DataTraining(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Tweet = db.Column(db.Text)
    label = db.Column(db.String(100))

    def __init__(self, Tweet, label):
        
        self.Tweet = Tweet
        self.label = label

class TesModelForm(FlaskForm):
    
    label = StringField('Label', validators=[DataRequired()])
    Tweet = StringField('Tweet', validators=[DataRequired()])
    submit = SubmitField('Simpan')