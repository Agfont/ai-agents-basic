variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "aws_profile" {
  description = "AWS SSO profile to use"
  type        = string
  default     = "AdministratorAccess-201181116727"
}

variable "project_name" {
  description = "Project name prefix for AWS resources"
  type        = string
  default     = "ai-agents-basic"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "VPC CIDR range"
  type        = string
  default     = "10.20.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Public subnet CIDR range"
  type        = string
  default     = "10.20.1.0/24"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "ec2_key_name" {
  description = "Optional EC2 key pair name for SSH"
  type        = string
  default     = null
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed for SSH"
  type        = string
  default     = "0.0.0.0/0"
}

variable "repo_url" {
  description = "Git URL to clone the repository on first boot"
  type        = string
}

variable "repo_branch" {
  description = "Repository branch to checkout on first boot"
  type        = string
  default     = "main"
}

variable "api_domain" {
  description = "Optional DNS domain for the API"
  type        = string
  default     = ""
}
