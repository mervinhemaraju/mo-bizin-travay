
locals {

  default_tags = {
    Environment = "prod"
    Application = "mo-bizin-travay"
    Owner       = "mervin.hemaraju"
    Creator     = "mervin.hemaraju"
    Project     = "https://github.com/mervinhemaraju/mo-bizin-travay"
    Terraform   = "Yes"
  }

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
