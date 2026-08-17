# IPRA — AWS Architecture (Participant 6)

## Logical Architecture
Internet → ALB → ECS (Frontend + API, private subnets) → Snowflake (external)
CloudWatch captures logs/metrics from ALB and ECS throughout.

## Deployment Architecture
- VPC `10.20.0.0/16` across 2 AZs.
- 2 public subnets: ALB only.
- 2 private subnets: ECS Fargate tasks (frontend + API).
- NAT Gateway: enabled in dev so API tasks can reach Snowflake/internet; documented cost trade-off.
- ALB: single internet-facing load balancer, path-based routing (`/api/*` → API target group, everything else → frontend).

## Data Flow
1. Browser requests the ALB DNS name.
2. `/` and static assets → frontend target group → React (nginx) container.
3. `/api/*` → API target group → FastAPI container → Snowflake.
4. API responses render inside the React app.

## Integration Flow
Participant 3 (Snowflake) → Participant 4 (API) → Participant 5 (React) → **Participant 6 (this module: containerize + deploy)** → Participant 8 (QA validates the deployed environment).
