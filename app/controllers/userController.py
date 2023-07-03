from app import app
from flask import request, jsonify, render_template, redirect, session
from flask_marshmallow import Marshmallow
from app.models.userModel import db, Users
from flask_jwt_extended import *
import datetime

ma = Marshmallow(app)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id_user', 'nama_user', 'username',
                  'email', 'password',  'no_hp', 'gender')


# init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


def getDetailUser(decodeToken):
    decode = decodeToken
    user = Users.query.get(decode.get('id_user'))
    result = user_schema.dump(user)
    return jsonify({"msg": "Success get user by id", "status": 200, "data": result})


def updateUser(decodeToken):
    decode = decodeToken
    user = Users.query.get(decode.get('id_user'))
    nama_user = request.form['nama_user']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    no_hp = request.form['no_hp']

    user.nama_user = nama_user
    user.username = username
    user.email = email
    user.no_hp = no_hp
    user.setPassword(password)
    db.session.commit()
    result = user_schema.dump(user)
    return jsonify({"msg": "Success update user", "status": 200, "data": result})


def signUp():
    nama_user = request.form['nama_user']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    no_hp = request.form['no_hp']
    gender = request.form['gender']

    newUser = Users(nama_user, username, email, no_hp, gender)
    newUser.setPassword(password)
    db.session.add(newUser)
    db.session.commit()
    user = user_schema.dump(newUser)
    return jsonify({"msg": "Success Sign Up", "status": 200, "data": user})


def signIn():
    username = request.form['username']
    password = request.form['password']

    user = Users.query.filter_by(username=username).first()

    if not user:
        return jsonify("User not found")

    if not user.checkPassword(password):
        error = "Gagal, username dan password tidak cocok"
        return render_template('login.html', error=error)
        # resp = jsonify({
        #     "status": 401,
        #     "msg": "Login Invalid",
        #     "error": "wrong password"
        # })
        resp.status_code = 500
        return resp
    session['logged_in'] = True
    data = singleTransform(user)
    expires = datetime.timedelta(days=1)
    expires_refresh = datetime.timedelta(days=3)
    access_token = create_access_token(data, fresh=True, expires_delta=expires)
    refresh_token = create_refresh_token(data, expires_delta=expires_refresh)
    newData = {**data, "token": access_token, "refresh_token": refresh_token}
    return redirect('/homeAdmin')


def refresh():
    user = get_jwt_identity()
    new_token = create_access_token(identity=user, fresh=False)

    return jsonify({
        "token_access": new_token
    }, "")


def singleTransform(users):
    return{
        'id_user': users.id_user,
        'nama_user': users.nama_user,
        'username': users.username,
        'password' : users.password,
        'email': users.email,
        'no_hp': users.no_hp,
        'gender': users.gender
    }
