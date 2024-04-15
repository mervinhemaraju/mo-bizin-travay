from main import main
# from test import main

CONTEXT = {}

EVENT_JOBS_MU = {
    "dry_run": True,
    "filters": {
        "wrapper": "div#wrapper",
        "openings": "div.utf-listings-container-part.compact-list-layout a.utf-job-listing",
        "name": "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description h3.utf-job-listing-title",
        "posted_date": "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description div.utf-job-listing-footer ul li:nth-child(4) span",
        "closing_date": "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description div.utf-job-listing-footer ul li:nth-child(5) span",
        "recruiter": "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description div.utf-job-listing-footer ul li:nth-child(1) span",
        "salary_range": "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description div.utf-job-listing-footer ul li:nth-child(3) span",
        "location": "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description div.utf-job-listing-footer ul li:nth-child(2) span",
        "link": "a.utf-job-listing",
        "pagination_button": 'nav.pagination ul li[data-arrow="right"] a',
    },
}

EVENT_MYJOB_MU = {
    "dry_run": True,
    "filters": {
        "wrapper": "div#page",
        "openings": "div.module.job-result",
        "name": "div.module-content div.job-result-logo-title div.job-result-title h2 a",
        "posted_date": "div.module-content div.job-result-overview ul.job-overview li.updated-time",
        "closing_date": "div.module-content div.job-result-overview ul.job-overview li.closed-time",
        "recruiter": "div.module-content div.job-result-logo-title div.job-result-title h3 a",
        "salary_range": "div.module-content div.job-result-overview ul.job-overview li.salary",
        "location": "div.module-content div.job-result-overview ul.job-overview li.location",
        "link": "div.module-content div.job-result-logo-title div.job-result-title h2 a",
        "pagination_button": "ul#pagination li:last-child a",
    },
}


EVENT_MCB_MU = {
    "dry_run": True,
    "filters": {
        "wrapper": "div.search-results-jobs-list.jobs-list",
        "openings": "div.job-tile.job-list-item",
        "name": "div.job-tile.job-list-item span.job-tile__title",
        "posted_date": "div.job-tile__subheader span i18n span span",
        "closing_date": "na",
        "recruiter": "MCB",
        "salary_range": "na",
        "location": "na",
        "link": "div.job-tile.job-list-item a.job-list-item__link",
        "pagination_button": "na",
    },
}

EVENT_ABSA_MU = {
    "dry_run": True,
    "filters": {
        "wrapper": "section.css-8j5iuw",
        "openings": "li.css-1q2dra3",
        "name": "li.css-1q2dra3 div.css-qiqmbt div.css-b3pn3b h3 a.css-19uc56f",
        "posted_date": "li.css-1q2dra3 div.css-zoser8 div.css-1y87fhn div.css-k008qs dd.css-129m7dg",
        "closing_date": "na",
        "recruiter": "ABSA",
        "salary_range": "na",
        "location": "na",
        "link": "li.css-1q2dra3 div.css-qiqmbt div.css-b3pn3b h3 a.css-19uc56f",
        "pagination_button": "na",
    },
}

if __name__ == "__main__":
    main(EVENT_ABSA_MU, CONTEXT)
