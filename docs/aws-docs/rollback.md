# Rollback Runbook

Every deployed image is tagged with its Git short SHA (`ipra-api:<sha>`, `ipra-frontend:<sha>`), so any previous version can be redeployed without rebuilding.

## Steps
1. Identify the previous known-good tag:
   ```
   aws ecr describe-images --repository-name ipra-dev-api \
     --query 'sort_by(imageDetails,& imagePushedAt)[-5:].imageTags'
   ```
2. Update the task definition to the previous image and register a new revision:
   ```
   aws ecs describe-task-definition --task-definition ipra-dev-api --query taskDefinition > td.json
   jq --arg IMAGE "<account>.dkr.ecr.us-east-1.amazonaws.com/ipra-dev-api:<previous-sha>" \
     '.containerDefinitions[0].image = $IMAGE | del(.taskDefinitionArn,.revision,.status,.requiresAttributes,.compatibilities,.registeredAt,.registeredBy)' \
     td.json > td-rollback.json
   aws ecs register-task-definition --cli-input-json file://td-rollback.json
   ```
3. Point the service at the new (rollback) revision:
   ```
   aws ecs update-service --cluster ipra-dev-cluster --service ipra-dev-api \
     --task-definition ipra-dev-api --force-new-deployment
   ```
4. Wait for stability and re-run smoke tests:
   ```
   aws ecs wait services-stable --cluster ipra-dev-cluster --services ipra-dev-api
   curl -f http://<alb-dns>/api/v1/health
   ```
5. Record the incident/change (what broke, which tag was restored, timestamps).

Repeat the same pattern for the frontend service with `ipra-dev-frontend`.
