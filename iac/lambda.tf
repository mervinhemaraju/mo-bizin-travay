
# * Lambda Function module
module "openings_scraping" {

  for_each = { for target in local.all_targets : target.recruiter => target }

  # * source module info
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 4"

  # * Function basic info
  function_name = "${local.lambda.prefix_name}-${lower(each.key)}"
  description   = "The lambda function Mo Bizin Travay for the recruiter ${each.key}"
  handler       = "main.main"

  # * Function advance info
  memory_size                       = 512
  cloudwatch_logs_retention_in_days = 14

  timeout                   = 60
  create_async_event_config = false
  maximum_retry_attempts    = 0

  # * Policies attachment
  create_role = false
  lambda_role = aws_iam_role.lambda.arn

  create_package = false
  package_type   = "Image"
  image_uri      = "${module.mo_bizin_travay_scraper.repository_url}:prod"

  hash_extra = trimprefix(data.aws_ecr_image.mobizintravay.id, "sha256:")

  # * Environment Variables
  environment_variables = {
    DB_TABLE_NAME      = var.db_table_name
    DELAY              = each.value.delay
    URL                = each.value.url
    PRINCIPAL_FILTER   = each.value.principal_filter
    FILTER_NAME        = each.value.filter_name
    FILTER_POSTED_DATE = each.value.filter_posted_date
    FILTER_LINK        = each.value.filter_link
    RECRUITER          = each.key
  }

  trusted_entities = [
    {
      type = "Service",
      identifiers = [
        "lambda.amazonaws.com"
      ]
    }
  ]
}

