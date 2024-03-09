
# * Lambda Function module
module "openings_scraping" {

  for_each = { for target in locals.all_targets : target.recruiter => target }

  # * source module info
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 4"

  # * Function basic info
  function_name = "mo-bizin-travay-${lower(each.key)}"
  description   = "The lambda function Mo Bizin Travay for the recruiter ${each.key}"
  handler       = "main.main"
  runtime       = "python3.11"

  # * Function advance info
  memory_size                       = 128
  cloudwatch_logs_retention_in_days = 14

  # * Source code
  source_path = "./scripts/scraper/"

  timeout                   = 600
  create_async_event_config = false
  maximum_retry_attempts    = 0

  # * Policies attachment
  policies           = [aws_iam_policy.lambda_actions.arn]
  attach_policies    = true
  number_of_policies = 1

  # * Publish the function
  publish = true

  trusted_entities = [
    {
      type = "Service",
      identifiers = [
        "lambda.amazonaws.com"
      ]
    }
  ]
}
