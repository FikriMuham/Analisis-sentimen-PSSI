from app import db

class UploadData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    data = db.Column(db.LargeBinary)

    def __init__(self, name, data):
        self.name = name
        self.data = data

