# Networking

| Resource | CIDR / Detail |
|---|---|
| VPC | 10.20.0.0/16 |
| Public subnet A | 10.20.0.0/24 (us-east-1a) |
| Public subnet B | 10.20.1.0/24 (us-east-1b) |
| Private subnet A | 10.20.10.0/24 (us-east-1a) |
| Private subnet B | 10.20.11.0/24 (us-east-1b) |

Routing:
- Public route table: `0.0.0.0/0` → Internet Gateway.
- Private route table: `0.0.0.0/0` → NAT Gateway (only if `enable_nat_gateway = true`).

Security groups:
- `alb-sg`: inbound 80/443 from `0.0.0.0/0`.
- `frontend-sg`: inbound container port only from `alb-sg`.
- `api-sg`: inbound container port only from `alb-sg`.

No ECS task has a public IP; the ALB is the only public entry point.
