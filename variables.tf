variable "bucket_name" {
  description = "Name of the s3 bucket. Must be unique."
  type        = string
  default     = "assign-3-bucket-adh"
}

variable "tags" {
  description = "Tags to set on the bucket."
  type        = map(string)
  default     = {}
}