from app import app
from flask import request, render_template, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import userController, tesModelController, uploadDataController, sentimenController, modelController
from app.models.tesModel import db, TesModel, TesModelForm



@app.route('/user', methods=['GET', 'PUT'])
@jwt_required()
def userDetails():
    current_user = get_jwt_identity()
    if(request.method == 'GET'):
        return userController.getDetailUser(current_user)
    if(request.method == 'PUT'):
        return userController.updateUser(current_user)

@app.route('/signup', methods=['POST'])
def signUp():
    return userController.signUp()

@app.route('/login', methods=['POST', 'GET'])
def login():
    if(request.method == 'GET'):
        return render_template('login.html')
    elif(request.method == 'POST'):
        session.pop('logged_in', None)
        return userController.signIn()
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/sentimen', methods=['GET'])
def sentimen():
    return render_template('klasifikasinv.html')

@app.route('/sentimen/result', methods=['GET','POST'])
def sentimenResult():
    return sentimenController.klasifikasi()

@app.route('/help', methods=['GET','POST'])
def help():
    return render_template('help.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/homeAdmin', methods=['GET'])
def homeAdmin():
    if session.get('logged_in') :
        return render_template('homeAdmin.html')
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)

@app.route('/klasifikasiAdmin', methods=['GET'])
def klasifikasiAdmin():
    if session.get('logged_in') :
        return render_template('klasifikasiAdmin.html')
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)

@app.route('/preprocessingAdmin', methods=['GET'])
def preprocessingAdmin():
    if session.get('logged_in') :
        return render_template('preprocessingAdmin.html')
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)

@app.route('/admin-preprocessing/result', methods=['GET'])
def preprocessingResultAdmin():
    if session.get('logged_in') :
        return render_template('preprocessingAdmin.html')
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)

@app.route('/', methods=['GET', 'POST'])
def tesmodel():
    if(request.method == 'GET'):
        return render_template('tesmodel.html')
    elif(request.method == 'POST'):
        return tesModelController.addTesModel()

@app.route('/tesmodel/result', methods=['GET', 'POST'])
def tesmodelResult():
        return tesModelController.tesmodel()  

@app.route('/tesmodelAdmin', methods=['GET'])
def tesmodelAdmin():
    if session.get('logged_in') :
        return tesModelController.getTesModelAdmin()
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)

@app.route('/tesmodelAdmin/result', methods=['GET', 'POST'])
def tesmodeAdminlResult():
    if session.get('logged_in') :
        return tesModelController.tesmodelAdmin()
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)

@app.route('/editTesModel/<id>', methods=['GET', 'POST'])
def editTesModel(id):
        tes_model = TesModel.query.get_or_404(id)
        form = TesModelForm(obj=tes_model)
        if request.method == 'POST' and form.validate_on_submit():
            form.populate_obj(tes_model)
            db.session.commit()
            flash('Tes Model updated successfully!', 'success')
            return redirect(url_for('tesmodelAdmin'))  # Redirect to the appropriate route after successful update
        return render_template('editTesModel.html', form=form, tes_model=tes_model)  # Pass 'tes_model' to the template


@app.route('/hapustesmodel/<tweet>', methods=['GET', 'POST'])
def hapustesmodel(tweet):
    # try:
        tes_model = TesModel.query.filter_by(tweet=tweet).first()
        # if tes_model:
        db.session.delete(tes_model)
        db.session.commit()
        flash('Berhasil Dihapus!')
        return redirect(url_for('tesmodelAdmin'))

@app.route('/tambahDataAdmin', methods=['GET', 'POST'])
def tambahDataAdmin():
    if session.get('logged_in') :
        if(request.method == 'GET'):
            return render_template('tambahDataAdmin.html')
        elif(request.method == 'POST'):
            return uploadDataController.uploadData()
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)
    
# @app.route('/gabungdata', methods=['POST'])
# def gabungdata():
#     if session.get('logged_in') :
#         return modelController.gabung_tabel()
#     else :
#         error = "Anda Belum Login"
#         return render_template('login.html', error=error)

@app.route("/exportCSV", methods=['GET'])
def exportCSV():
    return tesModelController.exportToCSV()