data "aws_caller_identity" "current" {}

data "aws_dynamodb_table" "mo_bizin_travay" {
  name = var.db_table_name
}

data "aws_ecr_image" "mobizintravay" {
  repository_name = "python/mo-bizin-travay/scraper"
  image_tag       = "prod"
}
