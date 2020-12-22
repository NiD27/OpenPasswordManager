import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from opm import app, db, bcrypt
from opm.forms import RegistrationForm, LoginForm, SettingsForm, CreateProfile
from opm.models import User , Profiles
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    profiles = Profiles.query.all()
    return render_template('dashboard.html',title='Dashboard', profiles=profiles)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created For {form.username.data}!','success')
        return redirect(url_for('signin'))
    return render_template('signup.html',title='Sign Up', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Failed! Please check login information!', 'danger')
    return render_template('signin.html',title='Sign In', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = SettingsForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account data updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account', image_file=image_file, form=form)

@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('signin'))

@app.route('/profile/new' , methods=['GET','POST'])
@login_required
def create_profile():
    form = CreateProfile()
    if form.validate_on_submit():
        profiles = Profiles(profile_name=form.profile_name.data, username=form.username.data, password=form.password.data, email=form.email.data, notes=form.notes.data, author=current_user)
        db.session.add(profiles)
        db.session.commit()
        flash('Profile successfully created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_profile.html',title='Create Profile',form=form, legend='Create Profile')

@app.route('/profile/<int:profile_id>')
def profile(profile_id):
    profile = Profiles.query.get_or_404(profile_id)
    if profile.author != current_user:
        abort(403)
    return render_template('profiles.html', title=profile.profile_name, profile=profile)

@app.route('/profile/<int:profile_id>/edit' , methods=['GET','POST'])
@login_required
def profile_edit(profile_id):
    profile = Profiles.query.get_or_404(profile_id)
    if profile.author != current_user:
        abort(403)
    form = CreateProfile()
    if form.validate_on_submit():
        profile.profile_name = form.profile_name.data
        profile.username = form.username.data
        profile.email = form.email.data
        profile.password = form.password.data
        profile.notes = form.notes.data
        db.session.commit()
        flash('Profile Updated Successfully!', 'success')
        return redirect(url_for('profile', profile_id=profile.id))
    elif request.method == 'GET':
        form.profile_name.data = profile.profile_name
        form.username.data = profile.username
        form.email.data = profile.email
        form.password.data = profile.password
        form.notes.data = profile.notes
    return render_template('create_profile.html', title='Edit Post', profile=profile, form=form, legend='Edit Profile')

@app.route('/profile/<int:profile_id>/delete' , methods=['POST'])
@login_required
def profile_delete(profile_id):
    profile = Profiles.query.get_or_404(profile_id)
    if profile.author != current_user:
        abort(403)
    db.session.delete(profile)
    db.session.commit()
    flash('Profile Deleted Successfully!', 'info')
    return redirect(url_for('dashboard'))
