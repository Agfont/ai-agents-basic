# Terraform EC2 Deployment

This Terraform stack provisions a minimal AWS environment for running `tutorial-api` on EC2 without Docker.

## What it creates

- VPC + public subnet + internet gateway + route table
- Security group (HTTP + HTTPS + SSH)
- IAM role/profile for SSM access
- EC2 instance (Ubuntu 22.04)
- Elastic IP attached to EC2
- Cloud-init bootstrap that installs:
  - Python + virtual environment
  - Nginx
  - Gunicorn
  - Certbot (Let's Encrypt)
  - `tutorial-api` systemd service

## AWS resources created

| Classification (AWS) | AWS service | Function |
| --- | --- | --- |
| Compute | Amazon EC2 Instance (`aws_instance.api`) | Runs the API service, Nginx proxy, and certbot automation. |
| Networking & Content Delivery | Amazon VPC (`aws_vpc.main`) | Creates the isolated network for all infrastructure components. |
| Networking & Content Delivery | Amazon VPC Subnet (`aws_subnet.public`) | Hosts the EC2 instance in a public subnet range. |
| Networking & Content Delivery | Amazon VPC Route Table (`aws_route_table.public`) | Routes outbound traffic (0.0.0.0/0) to the internet gateway. |
| Networking & Content Delivery | Route Table Association (`aws_route_table_association.public`) | Attaches the public subnet to the public route table. |
| Networking & Content Delivery | Internet Gateway (`aws_internet_gateway.main`) | Provides internet access path for resources in the VPC. |
| Networking & Content Delivery | Elastic IP (`aws_eip.api`) | Provides a stable public IPv4 address for DNS mapping and external access. |
| Security, Identity, & Compliance | AWS IAM Role (`aws_iam_role.ec2_ssm_role`) | Grants EC2 permissions to use AWS Systems Manager (SSM). |
| Security, Identity, & Compliance | IAM Role Policy Attachment (`aws_iam_role_policy_attachment.ssm_core`) | Attaches `AmazonSSMManagedInstanceCore` policy to the EC2 IAM role. |
| Security, Identity, & Compliance | IAM Instance Profile (`aws_iam_instance_profile.ec2_profile`) | Binds the IAM role to the running EC2 instance. |
| Security, Identity, & Compliance | Security Group (`aws_security_group.api`) | Controls inbound HTTP/HTTPS/SSH and outbound traffic rules for the instance. |

## Prerequisites

- Terraform >= 1.6
- AWS credentials configured (`aws configure` or environment variables)
- Repository URL accessible from EC2 bootstrap

## AWS EC2 Key Pair
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
API_BASE_URL=$(terraform output -raw api_base_url)
curl "$API_BASE_URL/api/health"
# terraform apply -replace=aws_instance.your_instance_name to recreate the instance if needed
```

If `api_domain` and `letsencrypt_email` are set and DNS points to the Elastic IP, cloud-init will request a trusted TLS cert and enable HTTPS redirect automatically.

Then verify:

```bash
API_BASE_URL=$(terraform output -raw api_base_url)
curl "$API_BASE_URL/api/health"
```

## First-time app env setup on EC2

SSH into the instance:

```bash
cd ../..
ELASTIC_IP=$(terraform output -raw elastic_ip)
ssh -i infra/terraform/ai-agents-key.pem "ubuntu@$ELASTIC_IP"
```

Copy your local `.env` file to the instance:

```bash
scp -i infra/terraform/ai-agents-key.pem .env "ubuntu@$ELASTIC_IP:/home/ubuntu/ai-agents-basic/.env"
```

## Important notes

- Create `/home/ubuntu/ai-agents-basic/.env` on the instance with required variables (`OPENAI_API_KEY`, `OPENAI_API_BASE`, etc.).
- For production, restrict `allowed_ssh_cidr` to your office IP/VPN CIDR.
- This setup keeps complexity low while enabling trusted HTTPS on EC2 with your own domain.

## DNS steps outside Terraform

If your DNS is not managed by this Terraform stack, do this in your DNS provider dashboard:

1. Create an `A` record for your API host (for example, `api.healthymarketbr.com`) pointing to Terraform output `elastic_ip`.
2. Wait for DNS propagation.
3. Run `terraform apply -replace=aws_instance.api` so cloud-init retries cert issuance with DNS already in place.

Notes:

- Let's Encrypt uses HTTP challenge on port 80, so keep port 80 open.
- If DNS is not pointing yet, the instance keeps serving HTTP until cert issuance succeeds.
