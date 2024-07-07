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

# @app.route('/sports//<path:path>', methods=["GET", "POST", "DELETE", "UPDATE"])
# def redirect_sports(path):
#     if request.method == 'POST' and path == 'search':
#         return redirect(url_for('sports.search_sports'))
#     elif request.method in ['GET', 'PATCH']:
#         return redirect(url_for('sports.handle_sport', path=path))
#     else:
#         return "Invalid route", 404

# @app.route('/events/', methods=["GET", "POST", "DELETE", "UPDATE"])
# def events_view():
#     pass

# @app.route('/selections/', methods=["GET", "POST", "DELETE", "UPDATE"])
# def selections_view():
#     pass

# # Register the other blueprints
# def register_blueprints(app):
#     app.register_blueprint(app)
#     app.register_blueprint(sports_bp, url_prefix='/sports')
#     app.register_blueprint(events_bp, url_prefix='/events')
#     app.register_blueprint(selections_bp, url_prefix='/selections')
