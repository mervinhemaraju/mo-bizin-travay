
resource "aws_scheduler_schedule_group" "lambda_trigger" {
  name = local.schedule_group.name
}

resource "aws_scheduler_schedule" "lambda_scheduler" {
  for_each = { for target in local.all_targets : target.recruiter => target }

  name                = "schedule-${local.lambda.prefix_name}-${lower(each.key)}"
  description         = "The schedule for ${local.lambda.prefix_name}-${lower(each.key)}"
  group_name          = aws_scheduler_schedule_group.lambda_trigger.name
  schedule_expression = "rate(6 days)"
  state               = "ENABLED"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:${local.lambda.prefix_name}-${lower(each.key)}"
    role_arn = aws_iam_role.scheduler.arn

    retry_policy {
      maximum_retry_attempts = 0
    }
  }

  depends_on = [module.openings_scraping, aws_scheduler_schedule_group.lambda_trigger]
}
