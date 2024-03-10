
# Lambda IAM Policy
resource "aws_iam_policy" "lambda" {

  name        = "mo-bizin-travay-actions"
  path        = "/"
  description = "The lambda actions for the project mo-bizin-travay"
  policy      = templatefile("${path.module}/policies/iam_lambda_role_actions.json", { dynamodb_arn = data.aws_dynamodb_table.mo_bizin_travay.arn })
}

# Lambda IAM Role
resource "aws_iam_role" "lambda" {
  name                = "mo-bizin-travay-lambda-role"
  description         = "The lambda role for the project mo-bizin-travay"
  assume_role_policy  = file("${path.module}/policies/iam_lambda_role_trust.json")
  managed_policy_arns = [aws_iam_policy.lambda.arn]

  depends_on = [aws_iam_policy.lambda]
}


# Scheduler IAM Role
resource "aws_iam_role" "scheduler" {
  name                = "mo-bizin-travay-scheduler-role"
  description         = "The scheduler role for the project mo-bizin-travay"
  assume_role_policy  = file("${path.module}/policies/iam_scheduler_role_trust.json")
  managed_policy_arns = [aws_iam_policy.scheduler.arn]

  depends_on = [aws_iam_policy.scheduler]
}

# Scheduler IAM Policy
resource "aws_iam_policy" "scheduler" {

  name        = "mo-bizin-travay-scheduler-policy"
  path        = "/"
  description = "The scheduler actions for the project mo-bizin-travay"
  policy = templatefile(
    "${path.module}/policies/iam_scheduler_role_actions.json",
    {
      lambda_arn = "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:mo-bizin-travay-*",
      iam_arn    = aws_iam_role.lambda.arn
    }
  )

  depends_on = [aws_iam_role.lambda]
}
