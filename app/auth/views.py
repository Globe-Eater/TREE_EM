from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from werkzeug.utils import secure_filename
import os
from . import auth
from .. import db
from ..models import User, Image
from .forms import LoginForm, MenuForm, UploadForm

@auth.route('/login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('auth.menu'))
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def acc_logout():
    logout_user()
    flash('You have been successfully logged out.')
    return redirect(url_for('main.index'))

@auth.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    form = MenuForm()
    if form.validate_on_submit():
        if form.upload_images.data:
            return redirect(url_for('auth.upload'))
        elif form.view_images.data:
            return redirect(url_for('auth.view_images'))
    return render_template('auth/menu.html', form=form)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/image_upload', methods=['GET', 'POST'])
def upload():
    UPLOAD_FOLDER = 'app/static/Stored_Images/'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            picture = Image(image_path=filename, owner_id=current_user.id)
            print(current_user)
            db.session.add(picture)
            db.session.commit()
        return redirect('auth/menu.html')
    return render_template('auth/upload.html')

@auth.route('/image/<int:index>')
@login_required
def view_images(index):
    img = Image.query.filter_by(image_id=index).first()
    if not img:
        return 'Img Not Found!', 404
    return Response(img.picture)

