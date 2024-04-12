import os
from flask import Blueprint, render_template as HTML, request
from app.web.models.db.dao import Dao
from kink import di

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

    # Create dao object
    dao = Dao()

    # Get data for the current page
    data, total_pages, total_documents = dao.get_paginated_data(page=page, query=query)

    # data, total_pages, total_documents = (
    #     [
    #         # {
    #         #     "title": "Operational Risk Analyst | Risk SBU | April 2024",
    #         #     "posted_date": "2024-04-05",
    #         #     "closing_date": "N/A",
    #         #     "recruiter": "N/A",
    #         #     "location": "N/A",
    #         #     "salary_range": "N/A",
    #         #     "updated_at": "2024-04-11",
    #         #     "opening_source": "mcbmu",
    #         #     "link": "https://ekbd.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/job/1337",
    #         # }
    #     ],
    #     0,
    #     0,
    # )

    accumulated_jobs = min(page * dao.PER_PAGE, total_documents)

    return HTML(
        "search.html",
        query=query,
        data=data,
        page=page,
        total_pages=total_pages,
        total_documents=total_documents,
        accumulated_jobs=accumulated_jobs,
    )
