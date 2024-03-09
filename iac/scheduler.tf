
resource "aws_scheduler_schedule_group" "lambda_trigger" {
  name = local.schedule_group.name
}

resource "aws_scheduler_schedule" "lambda_scheduler" {

  for_each = { for lambda in openings_scraping : lambda.lambda_function_arn => lambda }

  name                = "schedule-${each.value.lambda_function_name}"
  description         = "The schedule for ${each.value.lambda_function_name}"
  group_name          = aws_scheduler_schedule_group.lambda_trigger.name
  schedule_expression = "rate(4 days)"
  state               = "ENABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = each.key
    role_arn = aws_iam_role.scheduler.arn

    retry_policy {
      maximum_retry_attempts = 0
    }
  }

  depends_on = [module.openings_scraping, aws_scheduler_schedule_group.lambda_trigger]
}
