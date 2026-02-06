# AWS Deployment Guide - Vocabulary Visualization App

This guide explains how to deploy your vocabulary app to AWS (Amazon Web Services) so it's accessible on the internet.

---

## Table of Contents

1. [Deployment Options Overview](#deployment-options-overview)
2. [Recommended: AWS Amplify (Easiest)](#option-1-aws-amplify-easiest)
3. [Option 2: EC2 + S3 (Most Control)](#option-2-ec2--s3-most-control)
4. [Option 3: Elastic Beanstalk (Balanced)](#option-3-elastic-beanstalk-balanced)
5. [Option 4: ECS + Fargate (Containerized)](#option-4-ecs--fargate-containerized)
6. [Database Considerations](#database-considerations)
7. [Cost Estimates](#cost-estimates)
8. [Security Best Practices](#security-best-practices)

---

## Deployment Options Overview

| Option | Difficulty | Cost/Month | Best For |
|--------|-----------|------------|----------|
| **AWS Amplify** | ⭐ Easy | $5-15 | Quick deployment, beginners |
| **EC2 + S3** | ⭐⭐⭐ Medium | $10-30 | Full control, learning AWS |
| **Elastic Beanstalk** | ⭐⭐ Easy-Medium | $15-40 | Managed deployment |
| **ECS Fargate** | ⭐⭐⭐⭐ Hard | $20-50 | Production apps, scalability |

**My Recommendation**: Start with **AWS Amplify** - it's the easiest and cheapest way to get your app online.

---

## Option 1: AWS Amplify (Easiest)

### What is AWS Amplify?

Amplify is AWS's platform for deploying full-stack web apps. It handles:
- Frontend hosting (React app)
- Backend API (Flask app)
- Database (can use RDS or keep SQLite)
- SSL certificates (HTTPS)
- Custom domains
- Automatic deployments from Git

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                   AWS Amplify                        │
│                                                      │
│  ┌──────────────────┐      ┌──────────────────┐   │
│  │   Frontend       │      │    Backend       │   │
│  │   (React)        │◄────►│    (Flask)       │   │
│  │   CloudFront CDN │      │    Lambda/EC2    │   │
│  └──────────────────┘      └──────────────────┘   │
│                                     │               │
│                                     ▼               │
│                            ┌──────────────────┐   │
│                            │   Database       │   │
│                            │   RDS/SQLite     │   │
│                            └──────────────────┘   │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
              Your Domain
         https://vocab.yourdomain.com
```

### Prerequisites

1. **AWS Account** (free tier available)
   - Go to https://aws.amazon.com
   - Click "Create an AWS Account"
   - Provide credit card (won't be charged if you stay in free tier)

2. **Git Repository** (GitHub, GitLab, or Bitbucket)
   - Push your code to GitHub
   - Amplify will deploy from there

### Step-by-Step Deployment

#### Step 1: Prepare Your Code

First, we need to make a few changes for production:

**1. Create production requirements file**

Create `backend/requirements-prod.txt`:
```
Flask==3.0.0
Flask-CORS==4.0.0
SQLAlchemy==2.0.23
pandas==2.2.0
bcrypt==4.1.2
python-dotenv==1.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

**2. Create Procfile for backend**

Create `backend/Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT app.app:app
```

**3. Update backend configuration**

Update `backend/config/config.py` to use environment variables:
```python
import os

class Config:
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/vocabulary.db')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    # Session
    SESSION_DURATION_HOURS = int(os.getenv('SESSION_DURATION_HOURS', '24'))
```

**4. Update frontend API URL**

Update `frontend/src/api/client.ts`:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';
```

Create `frontend/.env.production`:
```
VITE_API_URL=https://your-api-url.amazonaws.com/api
```

#### Step 2: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for AWS deployment"

# Create GitHub repository (do this on github.com)
# Then push
git remote add origin https://github.com/yourusername/vocabulary-app.git
git branch -M main
git push -u origin main
```

#### Step 3: Deploy with Amplify

1. **Go to AWS Amplify Console**
   - Open https://console.aws.amazon.com/amplify
   - Click "Get Started" under "Amplify Hosting"

2. **Connect Repository**
   - Choose "GitHub"
   - Authorize AWS Amplify
   - Select your repository
   - Select branch: `main`

3. **Configure Build Settings**

Amplify will detect your app. Update the build settings:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm install
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: frontend/dist
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
backend:
  phases:
    preBuild:
      commands:
        - cd backend
        - pip install -r requirements-prod.txt
    build:
      commands:
        - python -c "from app.database import init_db; init_db()"
  artifacts:
    baseDirectory: backend
    files:
      - '**/*'
```

4. **Configure Environment Variables**
   - Click "Environment variables"
   - Add:
     - `SECRET_KEY`: Generate random string (use: `python -c "import secrets; print(secrets.token_hex(32))"`)
     - `CORS_ORIGINS`: Your Amplify frontend URL (will get this after deployment)
     - `DATABASE_URL`: (optional, for RDS)

5. **Deploy**
   - Click "Save and deploy"
   - Wait 5-10 minutes
   - You'll get a URL like: `https://main.d1234abcd.amplifyapp.com`

6. **Update CORS**
   - Copy your Amplify URL
   - Go back to Environment variables
   - Update `CORS_ORIGINS` with your URL
   - Redeploy

#### Step 4: Test Your Deployment

1. Open your Amplify URL
2. Register a new account
3. Add vocabulary entries
4. Test all features

### Custom Domain (Optional)

1. **Buy a domain** (on Route 53, GoDaddy, Namecheap, etc.)
2. **In Amplify Console**:
   - Click "Domain management"
   - Click "Add domain"
   - Enter your domain: `vocab.yourdomain.com`
   - Follow DNS configuration steps
3. **Wait for SSL certificate** (automatic, takes ~15 minutes)
4. **Access your app**: `https://vocab.yourdomain.com`

### Automatic Deployments

Every time you push to GitHub:
1. Amplify detects the change
2. Automatically builds and deploys
3. Your app updates in ~5 minutes

```bash
# Make changes
git add .
git commit -m "Add new feature"
git push

# Amplify automatically deploys!
```

---

## Option 2: EC2 + S3 (Most Control)

### What You'll Use

- **EC2**: Virtual server for Flask backend
- **S3**: Storage for React frontend (static files)
- **CloudFront**: CDN for fast frontend delivery
- **RDS**: Managed PostgreSQL database (optional)
- **Route 53**: DNS management (optional)

### Architecture

```
┌──────────────┐
│   Route 53   │  (DNS)
└──────┬───────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│ CloudFront   │  │   EC2        │
│ (Frontend)   │  │  (Backend)   │
│              │  │              │
│  S3 Bucket   │  │  Flask API   │
│  React App   │  │  Port 5001   │
└──────────────┘  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │     RDS      │
                  │  PostgreSQL  │
                  └──────────────┘
```

### Step-by-Step Deployment

#### Part A: Deploy Backend on EC2

**Step 1: Launch EC2 Instance**

1. Go to EC2 Console: https://console.aws.amazon.com/ec2
2. Click "Launch Instance"
3. Configure:
   - **Name**: vocabulary-backend
   - **AMI**: Ubuntu Server 22.04 LTS
   - **Instance type**: t2.micro (free tier)
   - **Key pair**: Create new (download .pem file)
   - **Security group**: 
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere
     - Allow HTTPS (port 443) from anywhere
     - Allow Custom TCP (port 5001) from anywhere
4. Click "Launch instance"

**Step 2: Connect to EC2**

```bash
# Make key file secure
chmod 400 your-key.pem

# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

**Step 3: Install Dependencies**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Install Nginx (web server)
sudo apt install nginx -y

# Install Git
sudo apt install git -y
```

**Step 4: Deploy Backend Code**

```bash
# Clone your repository
cd /home/ubuntu
git clone https://github.com/yourusername/vocabulary-app.git
cd vocabulary-app/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create data directory
mkdir -p data

# Initialize database
python -c "from app.database import init_db; init_db()"
```

**Step 5: Configure Gunicorn (Production Server)**

Create `/etc/systemd/system/vocabulary-backend.service`:

```ini
[Unit]
Description=Vocabulary App Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/vocabulary-app/backend
Environment="PATH=/home/ubuntu/vocabulary-app/backend/venv/bin"
ExecStart=/home/ubuntu/vocabulary-app/backend/venv/bin/gunicorn \
    --workers 3 \
    --bind 0.0.0.0:5001 \
    app.app:app

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl start vocabulary-backend
sudo systemctl enable vocabulary-backend
sudo systemctl status vocabulary-backend
```

**Step 6: Configure Nginx**

Create `/etc/nginx/sites-available/vocabulary-backend`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # or EC2 public IP

    location /api {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/vocabulary-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Part B: Deploy Frontend on S3

**Step 1: Build Frontend**

On your local machine:

```bash
cd frontend

# Update API URL in .env.production
echo "VITE_API_URL=http://your-ec2-ip/api" > .env.production

# Build for production
npm run build

# This creates frontend/dist/ folder
```

**Step 2: Create S3 Bucket**

1. Go to S3 Console: https://console.aws.amazon.com/s3
2. Click "Create bucket"
3. Configure:
   - **Name**: vocabulary-app-frontend (must be globally unique)
   - **Region**: us-east-1
   - **Uncheck** "Block all public access"
   - Click "Create bucket"

**Step 3: Upload Frontend Files**

```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Upload files
cd frontend/dist
aws s3 sync . s3://vocabulary-app-frontend --acl public-read
```

**Step 4: Enable Static Website Hosting**

1. Go to your S3 bucket
2. Click "Properties"
3. Scroll to "Static website hosting"
4. Click "Edit"
5. Enable static website hosting
6. Index document: `index.html`
7. Error document: `index.html` (for React Router)
8. Save

**Step 5: Configure Bucket Policy**

Click "Permissions" → "Bucket Policy":

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::vocabulary-app-frontend/*"
    }
  ]
}
```

**Step 6: Access Your App**

Your app is now live at:
```
http://vocabulary-app-frontend.s3-website-us-east-1.amazonaws.com
```

#### Part C: Add CloudFront (CDN) - Optional

1. Go to CloudFront Console
2. Create distribution
3. Origin: Your S3 bucket
4. Enable HTTPS
5. Get CloudFront URL: `https://d123abc.cloudfront.net`

---

## Option 3: Elastic Beanstalk (Balanced)

### What is Elastic Beanstalk?

AWS service that automatically handles:
- Server provisioning
- Load balancing
- Auto-scaling
- Monitoring
- Deployments

### Quick Deploy

```bash
# Install EB CLI
pip install awsebcli

# Initialize
cd backend
eb init -p python-3.11 vocabulary-backend

# Create environment
eb create vocabulary-prod

# Deploy
eb deploy

# Open in browser
eb open
```

Elastic Beanstalk handles everything automatically!

---

## Option 4: ECS + Fargate (Containerized)

### What You'll Use

- **Docker**: Containerize your app
- **ECR**: Store Docker images
- **ECS**: Run containers
- **Fargate**: Serverless container hosting

### Prerequisites

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app.app:app"]
```

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Deploy Steps

1. Build Docker images
2. Push to ECR
3. Create ECS cluster
4. Create task definitions
5. Create services
6. Configure load balancer

(This is advanced - I can provide detailed steps if you choose this option)

---

## Database Considerations

### Option A: Keep SQLite (Simplest)

**Pros**:
- No additional cost
- No setup needed
- Works immediately

**Cons**:
- Single file (can be lost if server crashes)
- Not scalable
- No concurrent writes

**Good for**: Personal use, testing

### Option B: Amazon RDS PostgreSQL (Recommended)

**Pros**:
- Managed service (automatic backups)
- Scalable
- Reliable
- Supports concurrent users

**Cons**:
- Costs $15-30/month
- Requires migration

**Setup**:

1. Create RDS instance (PostgreSQL)
2. Update `requirements.txt`: add `psycopg2-binary`
3. Update connection string:
   ```python
   DATABASE_URL = "postgresql://user:pass@rds-endpoint:5432/vocabdb"
   ```
4. Migrate data from SQLite to PostgreSQL

### Option C: Amazon DynamoDB (NoSQL)

**Pros**:
- Serverless (pay per request)
- Highly scalable
- Free tier available

**Cons**:
- Requires code changes (NoSQL vs SQL)
- Different query patterns

---

## Cost Estimates

### AWS Amplify (Recommended)

- **Build minutes**: $0.01/minute (first 1000 free)
- **Hosting**: $0.15/GB stored + $0.15/GB served
- **Typical cost**: $5-15/month

### EC2 + S3

- **EC2 t2.micro**: Free tier (1 year), then $8/month
- **S3**: $0.023/GB/month
- **Data transfer**: $0.09/GB
- **Typical cost**: $10-30/month

### Elastic Beanstalk

- **No additional cost** (you pay for underlying resources)
- **EC2 + Load Balancer**: $15-40/month

### ECS Fargate

- **vCPU**: $0.04048/hour
- **Memory**: $0.004445/GB/hour
- **Typical cost**: $20-50/month

### Free Tier Benefits (First 12 Months)

- EC2: 750 hours/month of t2.micro
- S3: 5GB storage
- RDS: 750 hours/month of db.t2.micro
- Lambda: 1M requests/month

---

## Security Best Practices

### 1. Use Environment Variables

Never hardcode:
- Database passwords
- API keys
- Secret keys

Use AWS Systems Manager Parameter Store or Secrets Manager.

### 2. Enable HTTPS

- Use AWS Certificate Manager (free SSL certificates)
- Force HTTPS redirects
- Enable HSTS headers

### 3. Restrict Access

- Use Security Groups (firewall rules)
- Only allow necessary ports
- Use IAM roles (not access keys)

### 4. Regular Backups

- Enable RDS automated backups
- Snapshot EC2 instances
- Version S3 buckets

### 5. Monitor and Log

- Enable CloudWatch logs
- Set up alarms for errors
- Monitor costs

---

## My Recommendation

For your vocabulary app, I recommend:

### Phase 1: Start Simple (AWS Amplify)
- **Cost**: $5-15/month
- **Time**: 1-2 hours
- **Difficulty**: Easy
- **Good for**: Getting online quickly, learning

### Phase 2: Scale Up (EC2 + RDS)
- **Cost**: $30-50/month
- **Time**: 4-6 hours
- **Difficulty**: Medium
- **Good for**: Multiple users, production use

### Phase 3: Enterprise (ECS + RDS + CloudFront)
- **Cost**: $100+/month
- **Time**: 1-2 days
- **Difficulty**: Hard
- **Good for**: Thousands of users, high availability

---

## Next Steps

1. **Choose your deployment option** (I recommend Amplify)
2. **Let me know** and I'll help you with detailed steps
3. **Prepare your code** (I can make the necessary changes)
4. **Deploy!**

Want me to help you deploy with AWS Amplify? Just say "Let's deploy with Amplify" and I'll guide you through each step!
