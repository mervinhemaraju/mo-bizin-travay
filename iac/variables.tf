
variable "region" {
  type        = string
  description = "The AWS target region."
  default     = "eu-west-1"
}

variable "db_table_name" {
  type        = string
  description = "The DB table name"
  default     = "mo-bizin-travay"
}
