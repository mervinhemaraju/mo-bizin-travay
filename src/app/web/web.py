import os
from kink import di
from flask import Blueprint, flash, redirect, url_for, request
from app.web.models.core.mbt import render_template as HTML
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
    # Create the api object
    api = MongoAPI()

    # Get the sources
    sources = api.get_sources()

    # Reformat the sources
    sources = [
        # if source ends with mu, add a dot before mu
        source.replace("mu", ".mu").upper()
        if source.lower().endswith("mu")
        else source.upper()
        for source in sources
    ]

    # Return the page with the sources
    return HTML("recruiters.html", sources=sources)


@web.route("/search")
def search():
    # Get the query
    query = request.args.get("query", "")

    # Get the sort
    sort = request.args.get("sort", None)
    sorting = []

    # Get current page from query parameters, default to 1
    page = int(request.args.get("page", 1))

    # Create the api object
    api = MongoAPI()

    # Define the sorting
    if sort is not None:
        # match case
        match sort:
            case "title":
                sorting.append([sort, 1])

            case "posted_date":
                sorting.append([sort, -1])

    # Get data for the current page
    data, total_pages, total_documents, per_page = api.get_paginated_data(
        page=page, query=query, sorting=sorting
    )

    accumulated_jobs = min(page * per_page, total_documents)

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
