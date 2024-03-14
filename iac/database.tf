resource "aws_dynamodb_table" "mo_bizin_travay" {
  name           = var.db_table_name
  billing_mode   = "PROVISIONED"
  read_capacity  = 15
  write_capacity = 10
  hash_key       = "id"

  stream_enabled = false

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "recruiter"
    type = "S"
  }


  global_secondary_index {
    name            = "recruiter_index"
    hash_key        = "recruiter"
    write_capacity  = 10
    read_capacity   = 10
    projection_type = "ALL"
  }
}
