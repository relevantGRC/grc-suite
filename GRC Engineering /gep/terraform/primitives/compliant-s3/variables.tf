
variable "project_name" {
  type        = string
  description = "Short project name used for bucket names and tags."

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,20}$", var.project_name))
    error_message = "Use 3-21 lowercase letters, numbers, or hyphens. Start with a letter."
  }
}

variable "environment" {
  type        = string
  description = "The environment in which this resource is deployed."

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Use dev, staging, or prod."
  }
}

variable "bucket_suffix" {
  type        = string
  description = "Optional custom S3 bucket suffix."
  default     = ""
}
