from flask import render_template, flash, redirect, Blueprint, url_for, request
from sportspro import create_app

from ..forms import LoginForm
# from .events import events_bp
# from .selections import selections_bp
# from .sports import sports_bp

app = create_app()

@app.route('/')
def home():
    return render_template('index.html', title='Home', user={}, posts={})

@app.route('/login')
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


# @app.route('/')
# def home():
#     return "Welcome to the Sportsbook Home Page"

# @app.route('/login')
# def login():
#     return "Login Page"

# @app.route('/signup')
# def signup():
#     return "Signup Page"

# alternative way to register blueprints in a neater way
# # Register the other blueprints
# def register_blueprints(app):
#     app.register_blueprint(app)
#     app.register_blueprint(sports_bp, url_prefix='/sports')
#     app.register_blueprint(events_bp, url_prefix='/events')
#     app.register_blueprint(selections_bp, url_prefix='/selections')
