from flask import redirect, url_for
from kink import di
from app.web.models.core.mbt import Mbt
from app.web.web import web

# * Create a Flask Application
app = Mbt()
app.config["SECRET_KEY"] = di["APP_SECRET_KEY"]

# * Register Blueprints
# > Web App Blueprints
app.register_blueprint(web, url_prefix="/web")


# * Redirect to the correct web page by default
@app.route("/")
@app.route("/web")
def page_web():
    return redirect(url_for("web.home_view"))
