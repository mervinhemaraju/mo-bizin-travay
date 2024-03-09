
# * Terraform Provider for AWS for the connection
provider "aws" {

  # * The AWS Environment Configurations
  region = var.region
}

# * The Terraform Module
terraform {

  # * Terraform version
  required_version = ">= 1.4.0"

  # * AWS Provider
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.66.0"
    }
  }
}
