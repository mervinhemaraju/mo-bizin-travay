
# * Lambda Function module
module "openings_scraping" {

  for_each = { for target in local.all_targets : target.recruiter => target }

  # * source module info
  source  = "spacelift.io/mervinhemaraju/module-terraform-aws-lambda/aws"
  version = "1.1.1"

  # * Function basic info
  function_name = "${local.lambda.prefix_name}-${lower(each.key)}"
  description   = "The lambda function Mo Bizin Travay for the recruiter ${each.key}"
  source_path   = null

  # * Function advance info
  memory_size = 512
  timeout     = 60

  # * Policies attachment
  lambda_role_arn = aws_iam_role.lambda.arn

  create_package = false
  image_uri      = data.aws_ecr_image.mobizintravay.image_uri

  # * Environment Variables
  environment_variables = {
    RECRUITER                = each.key
    DELAY                    = each.value.delay
    MAIN_URL                 = each.value.main_url
    CAREERS_URL              = each.value.careers_url
    WRAPPER_FILTER           = each.value.wrapper_filter
    OPENINGS_FILTER          = each.value.openings_filter
    FILTER_NAME              = each.value.filter_name
    FILTER_POSTED_DATE       = each.value.filter_posted_date
    FILTER_LINK              = each.value.filter_link
    FILTER_PAGINATION_BUTTON = each.value.filter_pagination_button
    DB_TABLE_NAME            = var.db_table_name
  }

  cron = "rate(6 days)"

  schedule_group = aws_scheduler_schedule_group.lambda_trigger.name

  schedule_role_arn = aws_iam_role.scheduler.arn
}

