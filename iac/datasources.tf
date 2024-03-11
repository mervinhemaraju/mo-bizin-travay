data "aws_caller_identity" "current" {}

data "aws_dynamodb_table" "mo_bizin_travay" {
  name = var.db_table_name
}

data "aws_ecr_image" "mobizintravay" {
  repository_name = local.ecr.repo_name
  image_tag       = "prod"
}
