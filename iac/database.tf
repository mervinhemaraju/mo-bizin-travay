resource "aws_dynamodb_table" "mo_bizin_travay" {
  name           = var.db_table_name
  billing_mode   = "PROVISIONED"
  read_capacity  = 25
  write_capacity = 25
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

  attribute {
    name = "opening_source"
    type = "S"
  }


  global_secondary_index {
    name            = "recruiter_index"
    hash_key        = "recruiter"
    write_capacity  = 10
    read_capacity   = 10
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "opening_source_index"
    hash_key        = "opening_source"
    write_capacity  = 10
    read_capacity   = 10
    projection_type = "ALL"
  }
}
