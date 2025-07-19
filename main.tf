resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.bucket_name
  tags   = var.tags
  force_destroy = true
}


resource "aws_dynamodb_table" "clowder" {
    name           = "clowder"
    read_capacity  = 5
    write_capacity = 5
    hash_key       = "Clowder_Id"

    attribute {
        name = "Clowder_Id"
        type = "S"
    }
}