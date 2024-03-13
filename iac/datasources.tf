data "aws_caller_identity" "current" {}

data "aws_ecr_image" "mobizintravay" {
  repository_name = local.ecr.repo_name
  most_recent     = true
}
