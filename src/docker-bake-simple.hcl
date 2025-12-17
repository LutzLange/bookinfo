// Simplified docker-bake.hcl for OTel-instrumented Bookinfo images
// Usage: cd src && docker buildx bake -f docker-bake-simple.hcl --push

variable "TAGS" {
  default = "latest"
}

variable "HUB" {
  default = "ghcr.io/lutzlange"
}

variable "PLATFORMS" {
  default = "linux/amd64,linux/arm64"
}

group "default" {
  targets = ["productpage", "details", "ratings", "reviews-v1", "reviews-v2", "reviews-v3"]
}

target "productpage" {
  context   = "./productpage"
  tags      = ["${HUB}/bookinfo-productpage:${TAGS}"]
  platforms = split(",", PLATFORMS)
}

target "details" {
  context   = "./details"
  tags      = ["${HUB}/bookinfo-details:${TAGS}"]
  platforms = split(",", PLATFORMS)
  args = {
    service_version = "v1"
  }
}

target "ratings" {
  context   = "./ratings"
  tags      = ["${HUB}/bookinfo-ratings:${TAGS}"]
  platforms = split(",", PLATFORMS)
  args = {
    service_version = "v1"
  }
}

target "reviews-v1" {
  context   = "./reviews"
  tags      = ["${HUB}/bookinfo-reviews:v1"]
  platforms = split(",", PLATFORMS)
  args = {
    service_version = "v1"
    enable_ratings  = "false"
  }
}

target "reviews-v2" {
  context   = "./reviews"
  tags      = ["${HUB}/bookinfo-reviews:v2"]
  platforms = split(",", PLATFORMS)
  args = {
    service_version = "v2"
    enable_ratings  = "true"
    star_color      = "black"
  }
}

target "reviews-v3" {
  context   = "./reviews"
  tags      = ["${HUB}/bookinfo-reviews:v3"]
  platforms = split(",", PLATFORMS)
  args = {
    service_version = "v3"
    enable_ratings  = "true"
    star_color      = "red"
  }
}
