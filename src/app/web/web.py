import os
from kink import di
from flask import Blueprint, flash, redirect, url_for, render_template as HTML, request
from app.web.models.services.mongoapi import MongoAPI
from app.web.models.core.functions import post_to_slack
from app.web.models.utils.slack_blocks import block_message

# * Create the web blueprint
web = Blueprint("web", __name__, static_folder="static", template_folder="templates")


# >>>> Main Pages <<<< #
@web.route("/")
def home_view():
    return HTML("index.html")


@web.route("/faq")
def faq():
    return HTML("faq.html")


@web.route("/contactus")
def contact_us():
    return HTML("contactus.html")


@web.route("/recruiters")
def recruiters():
    return HTML("recruiters.html")


@web.route("/search")
def search():
    # Get the query
    query = request.args.get("query", "")

    # Get current page from query parameters, default to 1
    page = int(request.args.get("page", 1))

    # Create the api object
    api = MongoAPI()

    # Get data for the current page
    data, total_pages, total_documents = api.get_paginated_data(page=page, query=query)

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

    accumulated_jobs = min(page * 10, total_documents)

    return HTML(
        "search.html",
        query=query,
        data=data,
        page=page,
        total_pages=total_pages,
        total_documents=total_documents,
        accumulated_jobs=accumulated_jobs,
    )


@web.route("/contact_submit", methods=["POST"])
def contact_us_submit():
    # Get the form data
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    # Post the message to slack
    post_to_slack(
        blocks=block_message(
            sender_name=name,
            sender_email=email,
            sender_subject=subject,
            message=message,
        )
    )

    # Send a flash message
    flash("Your message has been sent successfully!", "success")

    # Redirect back to the contact us form
    return redirect(url_for("web.contact_us"))
