from flask import Blueprint, render_template as HTML, request, current_app
from models.db.dao import Dao

# * Create the web blueprint
web = Blueprint("web", __name__, static_folder="static", template_folder="templates")


# >>>> Main Pages <<<< #
@web.route("/")
def home_view():
    return HTML("index.html")


@web.route("/search")
def search():
    # Get the query
    query = request.args.get("query", "")

    # Get current page from query parameters, default to 1
    page = int(request.args.get("page", 1))

    # # Create dao object
    # dao = Dao()

    # # Get data for the current page
    # data = get_paginated_data(page)

    return HTML("search.html", query=query, data=data, page=page)
