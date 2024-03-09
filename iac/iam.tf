
# Lambda IAM Policy
resource "aws_iam_policy" "lambda_actions" {

  name        = "mo-bizin-travay-actions"
  path        = "/"
  description = "The lambda actions for the project mo-bizin-travay"
  policy      = templatefile("${path.module}/policies/iam_lambda_role_actions.json", { dynamodb_arn = data.aws_dynamodb_table.mo_bizin_travay.arn })
}
