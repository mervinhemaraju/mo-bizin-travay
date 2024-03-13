
output "dynamodb_mo_bizin_travay_table_arn" {
  value = module.mo_bizin_travay_table.dynamodb_table_arn
}

output "dynamodb_mo_bizin_travay_table_id" {
  value = module.mo_bizin_travay_table.dynamodb_table_id
}
output "dynamodb_mo_bizin_travay_table_name" {
  value = var.db_table_name
}

