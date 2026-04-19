variable "aws_region"    {  default = "us-east-1" }
variable "environment"   {  default = "dev" }
variable "project_name"  {  default = "devops-p02" }
variable "app_image_tag" {  default = "latest" }

# These come from Project 1 outputs — paste your actual values here
variable "vpc_id"            { type = string }
variable "public_subnet_ids" { type = list(string) }

