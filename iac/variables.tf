
variable "region" {
  type        = string
  description = "The AWS target region."
  default     = "eu-west-1"
}

variable "db_table_name" {
  type        = string
  description = "The DB table name."
  default     = "mo-bizin-travay"
}

variable "slack_channel" {
  type        = string
  description = "The slack channel to post messages to."
  default     = "#mo-bizin-travay"
}

variable "token_doppler_iac_cloud_main" {
  type        = string
  description = "The token for secrets manager Doppler main project."
}
