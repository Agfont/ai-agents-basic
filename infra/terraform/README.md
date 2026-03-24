# Terraform EC2 Deployment

This Terraform stack provisions a minimal AWS environment for running `tutorial-api` on EC2 without Docker.

## What it creates

- VPC + public subnet + internet gateway + route table
- Security group (HTTP + SSH)
- IAM role/profile for SSM access
- EC2 instance (Ubuntu 22.04)
- Cloud-init bootstrap that installs:
  - Python + virtual environment
  - Nginx
  - Gunicorn
  - `tutorial-api` systemd service

## Prerequisites

- Terraform >= 1.6
- AWS credentials configured (`aws configure` or environment variables)
- Repository URL accessible from EC2 bootstrap

## AWS EC2 Key Pair
```bash
aws ec2 create-key-pair --key-name ai-agents-key --query KeyMaterial --output text > ai-agents-key.pem
chmod 400 ai-agents-key.pem 
```


## AWS SSO Access
```bash
aws sso login --profile <your-profile-name>
```

## Usage

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars

curl https://checkip.amazonaws.com # IPv4
curl https://checkip.global.api.aws  # IPv6
# edit terraform.tfvars with your values

terraform init
terraform plan
terraform apply
```

After apply:

```bash
PUBLIC_IP=$(terraform output -raw public_ip)
curl "http://$PUBLIC_IP/api/health" 
# terraform apply -replace=aws_instance.your_instance_name to recreate the instance if needed
```

## First-time app env setup on EC2

SSH into the instance:

```bash
cd ../..
ssh -i infra/terraform/ai-agents-key.pem "ubuntu@$PUBLIC_IP"
```

Copy your local `.env` file to the instance:

```bash

scp -i infra/terraform/ai-agents-key.pem .env "ubuntu@$PUBLIC_IP:/home/ubuntu/ai-agents-basic/.env"
```

Restart and verify the API service:

```bash
ssh -i infra/terraform/ai-agents-key.pem "ubuntu@$PUBLIC_IP"
sudo systemctl restart tutorial-api
sudo systemctl --no-pager --full status tutorial-api | sed -n '1,20p'
curl -f http://127.0.0.1:5050/api/health
```

Exit SSH and verify from your machine:

```bash
curl -f "http://$PUBLIC_IP/api/health"
```

## Important notes

- Create `/home/ubuntu/ai-agents-basic/.env` on the instance with required variables (`OPENAI_API_KEY`, `OPENAI_API_BASE`, etc.).
- For production, restrict `allowed_ssh_cidr` to your office IP/VPN CIDR.
- This is a single-instance baseline. Add ALB + ASG + TLS for production HA.
