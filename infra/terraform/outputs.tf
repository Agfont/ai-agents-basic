output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.api.id
}

output "public_ip" {
  description = "EC2 public IP"
  value       = aws_instance.api.public_ip
}

output "api_base_url" {
  description = "Base URL to call the API"
  value       = "http://${aws_instance.api.public_ip}"
}
