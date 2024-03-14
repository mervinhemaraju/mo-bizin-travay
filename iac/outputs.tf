
output "dynamodb_mo_bizin_travay_table_arn" {
  value = aws_dynamodb_table.mo_bizin_travay.arn
}

output "dynamodb_mo_bizin_travay_table_id" {
  value = aws_dynamodb_table.mo_bizin_travay.id
}
output "dynamodb_mo_bizin_travay_table_name" {
  value = var.db_table_name
}

