output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.api.id
}

output "elastic_ip" {
  description = "Elastic IP attached to EC2"
  value       = aws_eip.api.public_ip
}

output "api_base_url" {
  description = "Base URL to call the API"
  value       = "https://${var.api_domain}"
}
