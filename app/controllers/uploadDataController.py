from app import app
from flask import request, jsonify, render_template, redirect
from flask_marshmallow import Marshmallow
from app.models.uploadData import db, UploadData

ma = Marshmallow(app)


class UploadDataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'data')


# init schema
uploadData_schema = UploadDataSchema()
uploadDatas_schema = UploadDataSchema(many=True)

def uploadData():
    file = request.files['file']
    newUploadData = UploadData(file.filename, file.read())
    db.session.add(newUploadData)
    db.session.commit()
    uploadData = uploadData_schema.dump(newUploadData)
    return jsonify({"msg": "Success add data", "status": 200, "data": uploadData})

def getAllUploadData():
    allUploadData = UploadData.query.order_by(UploadData.id).all()
    result = uploadDatas_schema.dump(allUploadData)
    return jsonify({"msg": "Success Get all data", "status": 200, "data": result})
