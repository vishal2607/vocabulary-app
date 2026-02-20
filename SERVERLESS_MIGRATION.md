# Serverless Migration Plan

## Current Architecture (Flask + SQLite)
- Backend: Flask on Elastic Beanstalk
- Database: SQLite
- Auth: Custom Flask sessions
- Frontend: React on Amplify

## New Architecture (Serverless)
- Backend: AWS Lambda + API Gateway
- Database: DynamoDB
- Auth: AWS Cognito
- Frontend: React on Amplify (same)

## Migration Steps

### Phase 1: Setup Infrastructure
1. Create DynamoDB tables
2. Setup Cognito User Pool
3. Create API Gateway
4. Setup Lambda functions

### Phase 2: Backend Migration
1. Convert Flask routes to Lambda functions
2. Migrate SQLite data model to DynamoDB
3. Replace custom auth with Cognito
4. Update API endpoints

### Phase 3: Frontend Updates
1. Replace axios client with AWS Amplify SDK
2. Update authentication flow
3. Update API calls to use API Gateway
4. Test end-to-end

### Phase 4: Deployment
1. Deploy Lambda functions
2. Deploy API Gateway
3. Update Amplify environment variables
4. Test production

## Cost Comparison

### Current (Elastic Beanstalk)
- EC2 instance: ~$15-30/month
- Load balancer: ~$18/month
- Total: ~$33-48/month (always running)

### Serverless
- Lambda: $0.20 per 1M requests (free tier: 1M requests/month)
- API Gateway: $3.50 per 1M requests (free tier: 1M requests/month)
- DynamoDB: $1.25 per 1M read requests (free tier: 25GB storage)
- Cognito: Free for <50,000 users
- Total: ~$0-5/month for personal use (pay per use)

## Timeline
- Setup: 1-2 hours
- Migration: 2-3 hours
- Testing: 1 hour
- Total: 4-6 hours
