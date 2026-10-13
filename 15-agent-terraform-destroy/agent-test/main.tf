terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
    }
  }
}

resource "local_file" "orders_db" {
  filename = "${path.module}/../cloud-direct-c/orders-db.txt"
  content  = "sample orders, test data\n"
}

resource "local_file" "shop_site" {
  filename = "${path.module}/../cloud-direct-c/shop-site.txt"
  content  = "shop website, version 1\n"
}
