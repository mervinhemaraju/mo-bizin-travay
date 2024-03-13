module "mo_bizin_travay_table" {

  # Module info
  source  = "terraform-aws-modules/dynamodb-table/aws"
  version = "4.0.0"

  # Basic DB Info
  name     = var.db_table_name
  hash_key = "id"

  # Capacity configs
  billing_mode   = "PROVISIONED"
  read_capacity  = 15
  write_capacity = 10

  # Attributes
  attributes = [
    {
      name = "id"
      type = "S"
    },
    {
      name = "posted_date"
      type = "S"
    },
    {
      name = "updated_at"
      type = "S"
    },
    {
      name = "recruiter"
      type = "S"
    },
  ]

  # GSI
  global_secondary_indexes = [
    {
      name            = "recruiter_index"
      hash_key        = "recruiter"
      projection_type = "ALL"
    },
    {
      name            = "posted_date_index"
      hash_key        = "posted_date"
      projection_type = "ALL"
    },
    {
      name            = "updated_at_index"
      hash_key        = "updated_at"
      projection_type = "ALL"
    }
  ]
}
