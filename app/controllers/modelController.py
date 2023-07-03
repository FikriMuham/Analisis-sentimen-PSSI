# from app import app, db
# from flask import request, jsonify, render_template, redirect
# from flask_marshmallow import Marshmallow
# from app.models.model import Sentimen

# ma = Marshmallow(app)

# class SentimenSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'Tweet', 'label')

# # init schema
# Sentimen_schema = SentimenSchema()
# Sentimens_schema = SentimenSchema(many=True)


# def Add_gabung_tabel():
#     data = db.session.query(hasil_sentimen, tes_model).join(tes_model, hasil_sentimen.id == tes_model.id).all()
#     return render_template('tesModelAdmin.html', data=data)
