from flask import Flask, redirect, url_for
from app.web.web import web

# * Create a Flask Application
app = Flask(__name__)

# * Register Blueprints

# > Web App Blueprints
app.register_blueprint(web, url_prefix="/home")


# * Redirect to the correct web page by default
@app.route("/")
@app.route("/home")
def page_web():
    return redirect(url_for("web.home_view"))
