
# * Lambda Function module
module "openings_scraping" {

  for_each = { for target in local.all_targets : target.source => target }

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
  image_uri      = data.aws_ecr_image.mobizintravay.image_uri

  # * Environment Variables
  # environment_variables = {
  #   RECRUITER                = each.key
  #   DELAY                    = each.value.delay
  #   MAIN_URL                 = each.value.main_url
  #   CAREERS_URL              = each.value.careers_url
  #   WRAPPER_FILTER           = each.value.wrapper_filter
  #   OPENINGS_FILTER          = each.value.openings_filter
  #   FILTER_NAME              = each.value.filter_name
  #   FILTER_POSTED_DATE       = each.value.filter_posted_date
  #   FILTER_LINK              = each.value.filter_link
  #   FILTER_PAGINATION_BUTTON = each.value.filter_pagination_button
  #   DB_TABLE_NAME            = var.db_table_name
  # }

  environment_variables = {
    DELAY              = 15
    SECRETS_MAIN_TOKEN = var.token_doppler_iac_cloud_main
    SLACK_CHANNEL      = var.slack_channel
    DB_TABLE_NAME      = var.db_table_name
    SOURCE             = each.value.key
    SOURCE_URL         = each.value.source_url
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

