module "mo_bizin_travay_scraper" {
  source  = "terraform-aws-modules/ecr/aws"
  version = "1.6.0"

  repository_name = "python/mo-bizin-travay/scraper"

  #   repository_read_write_access_arns = ["arn:aws:iam::012345678901:role/terraform"]
  repository_lambda_read_access_arns = [
    "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:mo-bizin-travay-*"
  ]

  repository_force_delete = true

  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep last 5 images",
        selection = {
          tagStatus   = "any",
          countType   = "imageCountMoreThan",
          countNumber = 5
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}
