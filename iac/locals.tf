
locals {

  default_tags = {
    Environment = "prod"
    Application = "mo-bizin-travay"
    Owner       = "mervin.hemaraju"
    Creator     = "mervin.hemaraju"
    Project     = "https://github.com/mervinhemaraju/mo-bizin-travay"
    Terraform   = "Yes"
  }

  all_targets = [
    {
      source            = "jobsmu",
      source_url        = "https://www.jobs.mu/jobs",
      source_url_suffix = "",
      filters = {
        "wrapper" : "div#wrapper",
        "openings" : "div.utf-listings-container-part.compact-list-layout a.utf-job-listing",
        "name" : "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description h3.utf-job-listing-title",
        "posted_date" : "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description div.utf-job-listing-footer ul li:nth-child(4) span",
        "closing_date" : "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description div.utf-job-listing-footer ul li:nth-child(5) span",
        "recruiter" : "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description div.utf-job-listing-footer ul li:nth-child(1) span",
        "salary_range" : "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description div.utf-job-listing-footer ul li:nth-child(3) span",
        "location" : "a.utf-job-listing div.utf-job-listing-details div.utf-job-listing-description div.utf-job-listing-footer ul li:nth-child(2) span",
        "link" : "a.utf-job-listing",
        "pagination_button" : "nav.pagination ul li[data-arrow='right'] a",
      }
    },
    {
      source            = "myjobmu",
      source_url        = "https://www.myjob.mu",
      source_url_suffix = "/ShowResults.aspx?Keywords=&Location=&Category=&Recruiter=Company&Page=1",
      filters = {
        "wrapper" : "div#page",
        "openings" : "div.module.job-result",
        "name" : "div.module-content div.job-result-logo-title div.job-result-title h2 a",
        "posted_date" : "div.module-content div.job-result-overview ul.job-overview li.updated-time",
        "closing_date" : "div.module-content div.job-result-overview ul.job-overview li.closed-time",
        "recruiter" : "div.module-content div.job-result-logo-title div.job-result-title h3 a",
        "salary_range" : "div.module-content div.job-result-overview ul.job-overview li.salary",
        "location" : "div.module-content div.job-result-overview ul.job-overview li.location",
        "link" : "div.module-content div.job-result-logo-title div.job-result-title h2 a",
        "pagination_button" : "ul#pagination li:last-child a",
      }
    }
  ]

  # all_targets = [
  #   {
  #     recruiter                = "MCB",
  #     delay                    = 15,
  #     main_url                 = "https://ekbd.fa.em2.oraclecloud.com"
  #     careers_url              = "https://ekbd.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/requisitions?"
  #     wrapper_filter           = "div.search-results-jobs-list.jobs-list"
  #     openings_filter          = "div.job-tile.job-list-item"
  #     filter_name              = "div.job-tile.job-list-item span.job-tile__title"
  #     filter_posted_date       = "div.job-tile__subheader span i18n span span"
  #     filter_link              = "div.job-tile.job-list-item a.job-list-item__link"
  #     filter_pagination_button = "na"
  #   },
  #   {
  #     recruiter                = "CONCENTRIX",
  #     delay                    = 15,
  #     main_url                 = "https://jobs.concentrix.com"
  #     careers_url              = "https://jobs.concentrix.com/global/en/mauritius-search"
  #     wrapper_filter           = "div.phs-facet-results-block"
  #     openings_filter          = "li.jobs-list-item"
  #     filter_name              = "li.jobs-list-item div.wrapper-cntr div.information span a.au-target div.job-title span"
  #     filter_posted_date       = "li.jobs-list-item div.wrapper-cntr div.information p.job-info span.job-postdate"
  #     filter_link              = "li.jobs-list-item div.wrapper-cntr div.information span a.au-target"
  #     filter_pagination_button = "na"
  #   },
  #   {
  #     recruiter                = "SDWORX",
  #     delay                    = 15,
  #     main_url                 = "https://careers.sdworx.com"
  #     careers_url              = "https://careers.sdworx.com/jobs?country=Mauritius"
  #     wrapper_filter           = "div.bg-company-primary.z-career-jobs-list.jobs-list-container"
  #     openings_filter          = "li.w-full"
  #     filter_name              = "li.w-full a.flex.flex-col.py-6.text-center.focus-visible-company span"
  #     filter_posted_date       = "li.jobs-list-item div.wrapper-cntr div.information p.job-info span.job-postdate"
  #     filter_link              = "li.w-full a.flex.flex-col.py-6.text-center.focus-visible-company"
  #     filter_pagination_button = "div.bg-company-primary.z-career-jobs-list.jobs-list-container div a.careersite-button"
  #   },
  #   {
  #     recruiter                = "ABSA"
  #     delay                    = 15
  #     main_url                 = "https://absa.wd3.myworkdayjobs.com"
  #     careers_url              = "https://absa.wd3.myworkdayjobs.com/ABSAcareersite?locationCountry=a759018ba6ac489d9f16c086b914e1b6"
  #     wrapper_filter           = "section.css-8j5iuw"
  #     openings_filter          = "li.css-1q2dra3"
  #     filter_name              = "li.css-1q2dra3 div.css-qiqmbt div.css-b3pn3b h3 a.css-19uc56f"
  #     filter_posted_date       = "li.css-1q2dra3 div.css-zoser8 div.css-1y87fhn div.css-k008qs dd.css-129m7dg"
  #     filter_link              = "li.css-1q2dra3 div.css-qiqmbt div.css-b3pn3b h3 a.css-19uc56f"
  #     filter_pagination_button = "na"
  #   }
  # ]

  ecr = {
    repo_name = "python/mo-bizin-travay/scraper"
  }

  lambda = {
    prefix_name = "mo-bizin-travay"
  }

  schedule_group = {
    name = "mo-bizin-travay-schedules"
  }
}
