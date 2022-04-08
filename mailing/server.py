import os
from flask import Flask
from flask import render_template

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = "templates"

def build_application():
    app = Flask('MAil')
    app.static_folder = os.path.join(HERE, TEMPLATES)
    app.config.update(dict(
        DEBUG = True,
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = 'gregory.hannebique@gmail.com',
        MAIL_PASSWORD = 'P3j!r4m4Sh!m3n',
    ))

    @app.route("/")
    def index():
        INDEX_FILE = 'index.html'
        return render_template(INDEX_FILE)
    
    return app
