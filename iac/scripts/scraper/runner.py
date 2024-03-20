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

if __name__ == "__main__":
    main(EVENT_JOBS_MU, CONTEXT)
