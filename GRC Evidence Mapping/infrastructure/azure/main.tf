resource "azurerm_storage_account" "secure_data" {
  name                     = "storageeachub2026"
  resource_group_name      = "compliance-rg"
  location                 = "West US"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
