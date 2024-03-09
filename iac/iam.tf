
# Lambda IAM Policy
resource "aws_iam_policy" "lambda_actions" {

  name        = "mo-bizin-travay-actions"
  path        = "/"
  description = "The lambda actions for the project mo-bizin-travay"
  policy      = templatefile("${path.module}/policies/iam_lambda_role_actions.json", { dynamodb_arn = data.aws_dynamodb_table.mo_bizin_travay.arn })
}

# Scheduler IAM Role
resource "aws_iam_role" "scheduler" {
  name               = "mo-bizin-travay-scheduler-role"
  assume_role_policy = file("${path.module}/policies/iam_scheduler_role_trust.json")
}
