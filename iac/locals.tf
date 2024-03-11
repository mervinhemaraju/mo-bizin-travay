
locals {

  default_tags = {
    Environment = "prod"
    Application = "mo-bizin-travay"
    Owner       = "mervin.hemaraju"
    Creator     = "mervin.hemaraju"
    Project     = "https://github.com/mervinhemaraju/mo-bizin-travay"
  }

  all_targets = [
    {
      recruiter          = "MCB",
      delay              = 15,
      url                = "https://ekbd.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/requisitions?"
      principal_filter   = "job-list-item"
      filter_name        = "div.job-tile span.job-tile__title"
      filter_posted_date = "div.job-tile__subheader span i18n span span"
      filter_link        = "div.job-tile a.job-list-item__link"
    }
  ]

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
