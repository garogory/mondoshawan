# main.py
import folium
from geopy.geocoders import Nominatim

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import ResetPasswordRequestForm
from .mail import send_password_reset_email
from .models import Entry

main = Blueprint('main', __name__)
PIMPMYRUN = "pimpmyrun"

def build_new_map(address, latitude, longitude):
    center = [latitude, longitude]
    m = folium.Map(location=entry,  zoom_start=13)
    folium.Circle(radius=1000,
                  location=entry,
                  popup='The Waterfront',
                  color='crimson',
                  fill=False,
                 ).add_to(m)

    folium.Marker(center,
                  popup=location.address,
                  icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
    return m

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/adresses')
@login_required
def adresses():
    return render_template('adresses.html', name=current_user.name)

@main.route('/adresses', methods=['POST'])
@login_required
def adresses_post():
    address = request.form.get('address')
    geolocator = Nominatim(user_agent=PIMPMYRUN)
    location = geolocator.geocode(address)
    newentry = Entry.query.filter_by(address=location.address).first()
    if not newentry:
        flash('Please check your login details and try again.')
        return redirect(url_for('main.adresses')) # if user doesn't exist or password is wrong, reload the page

    add_new_entry(address, latitude, longitude)

    newmap = build_new_map(address, latitude, longitude)

    return newmap._repr_html_()

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)
