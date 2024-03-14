resource "aws_iam_user" "mo_bizin_travay" {
  name = "mo-bizin-travay"
  path = "/"
}

resource "aws_iam_user_policy" "mo_bizin_travay" {
  name = "iam-user-mo-bizin-travay-actions"
  user = aws_iam_user.mo_bizin_travay.name
  policy = templatefile(
    "${path.module}/policies/iam_user_mo_bizin_travay_actions.json",
    {
      dynamodb_arn = "${aws_dynamodb_table.mo_bizin_travay.arn}*"
    }
  )
}
