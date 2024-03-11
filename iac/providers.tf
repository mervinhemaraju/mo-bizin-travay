
# * Terraform Provider for AWS for the connection
provider "aws" {

  # * The AWS Environment Configurations
  region = var.region

  # * Set the default tags
  default_tags {
    tags = local.default_tags
  }
}

# * The Terraform Module
terraform {

  # * Terraform version
  required_version = ">= 1.4.0"

  # * AWS Provider
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.9"
    }
  }
}
