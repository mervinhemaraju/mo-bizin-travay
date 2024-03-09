module "openings_scraping" {

  for_each = { for target in locals.all_targets : target.recruiter => target }

  source  = "spacelift.io/cko-it/it-terraform-lambda-module/aws"
  version = "2.1.0"

  function_name = "mo-bizin-travay-${lower(each.key)}"
  description   = "The lambda function Mo Bizin Travay for the recruiter ${each.key}"

  policies_arns = [aws_iam_policy.lambda_actions.arn]

  memory_size = 128
  source_path = "./scripts/scraper/"

  timeout = "600"

}
