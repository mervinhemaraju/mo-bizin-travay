
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

  timeout                   = 600
  create_async_event_config = false
  maximum_retry_attempts    = 0

  # * Policies attachment
  create_role = false
  lambda_role = aws_iam_role.lambda.arn

  create_package = false
  package_type   = "Image"
  image_uri      = data.aws_ecr_image.mobizintravay.image_uri

  environment_variables = {
    DELAY              = 15
    SECRETS_MAIN_TOKEN = var.token_doppler_iac_cloud_main
    SLACK_CHANNEL      = var.slack_channel
    DB_TABLE_NAME      = var.db_table_name
    SOURCE             = each.key
    SOURCE_URL         = each.value.source_url
    SOURCE_URL_SUFFIX  = each.value.source_url_suffix
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

