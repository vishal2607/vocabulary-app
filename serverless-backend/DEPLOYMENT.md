# Serverless Backend Deployment Guide

## Prerequisites

1. **AWS CLI** installed and configured
2. **AWS SAM CLI** installed
3. **Python 3.11** installed
4. **AWS Account** with appropriate permissions

## Installation

### Install AWS SAM CLI

```bash
# macOS
brew install aws-sam-cli

# Or using pip
pip install aws-sam-cli
```

### Verify Installation

```bash
sam --version
aws --version
```

## Deployment Steps

### 1. Build the Application

```bash
cd serverless-backend
sam build
```

### 2. Deploy to AWS

First deployment (guided):
```bash
sam deploy --guided --profile vishal1-isengard
```

Answer the prompts:
- Stack Name: `vocabulary-app-serverless`
- AWS Region: `us-east-1`
- Confirm changes: `Y`
- Allow SAM CLI IAM role creation: `Y`
- Disable rollback: `N`
- Save arguments to config: `Y`

Subsequent deployments:
```bash
sam deploy --profile vishal1-isengard
```

### 3. Get Output Values

After deployment, SAM will output:
- **ApiEndpoint**: Your API Gateway URL
- **UserPoolId**: Cognito User Pool ID
- **UserPoolClientId**: Cognito Client ID

Save these values - you'll need them for the frontend!

## Testing the API

### Create a Test User

```bash
aws cognito-idp sign-up \
  --client-id YOUR_CLIENT_ID \
  --username test@example.com \
  --password TestPassword123! \
  --profile vishal1-isengard
```

### Confirm the User (admin)

```bash
aws cognito-idp admin-confirm-sign-up \
  --user-pool-id YOUR_USER_POOL_ID \
  --username test@example.com \
  --profile vishal1-isengard
```

### Get Auth Token

```bash
aws cognito-idp initiate-auth \
  --client-id YOUR_CLIENT_ID \
  --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME=test@example.com,PASSWORD=TestPassword123! \
  --profile vishal1-isengard
```

### Test API Endpoint

```bash
curl -X GET \
  https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/Prod/vocab \
  -H "Authorization: Bearer YOUR_ID_TOKEN"
```

## Monitoring

### View Logs

```bash
sam logs -n GetVocabFunction --stack-name vocabulary-app-serverless --tail --profile vishal1-isengard
```

### View in AWS Console

- Lambda: https://console.aws.amazon.com/lambda
- API Gateway: https://console.aws.amazon.com/apigateway
- DynamoDB: https://console.aws.amazon.com/dynamodb
- Cognito: https://console.aws.amazon.com/cognito

## Cleanup

To delete all resources:

```bash
sam delete --stack-name vocabulary-app-serverless --profile vishal1-isengard
```

## Cost Estimate

With AWS Free Tier:
- Lambda: 1M requests/month free
- API Gateway: 1M requests/month free
- DynamoDB: 25GB storage free
- Cognito: 50,000 MAU free

Expected cost for personal use: **$0-2/month**

## Next Steps

1. Deploy the backend using the commands above
2. Update frontend to use AWS Amplify SDK
3. Configure frontend with Cognito and API Gateway URLs
4. Test end-to-end
