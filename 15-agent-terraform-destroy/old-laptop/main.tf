terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
    }
  }
}

resource "local_file" "orders_db" {
  filename = "${path.module}/../cloud/orders-db.txt"
  content  = "2.5 years of customer orders\n"
}

resource "local_file" "shop_site" {
  filename = "${path.module}/../cloud/shop-site.txt"
  content  = "shop website, version 1\n"
}
