terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
    }
  }
}

resource "local_file" "orders_db" {
  filename = "${path.module}/../cloud-safe/orders-db.txt"
  content  = "2.5 years of customer orders\n"

  lifecycle {
    prevent_destroy = true
  }
}

resource "local_file" "shop_site" {
  filename = "${path.module}/../cloud-safe/shop-site.txt"
  content  = "shop website, version 1\n"
}
