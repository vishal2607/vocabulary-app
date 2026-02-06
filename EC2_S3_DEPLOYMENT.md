# EC2 + S3 Deployment Guide - Step by Step

This guide will walk you through deploying your vocabulary app using AWS EC2 (backend) and S3 (frontend).

---

## What You'll Deploy

```
┌─────────────────────────────────────────────────────┐
│                      AWS                             │
│                                                      │
│  ┌──────────────────┐      ┌──────────────────┐   │
│  │   S3 Bucket      │      │   EC2 Instance   │   │
│  │   (Frontend)     │◄────►│   (Backend)      │   │
│  │                  │      │                  │   │
│  │  React App       │      │  Flask API       │   │
│  │  Static Files    │      │  Gunicorn        │   │
│  │                  │      │  Nginx           │   │
│  └──────────────────┘      └──────────────────┘   │
│                                     │               │
│                                     ▼               │
│                            ┌──────────────────┐   │
│                            │   SQLite DB      │   │
│                            │   (on EC2)       │   │
│                            └──────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Result**: Your app will be accessible at:
- Frontend: `http://your-bucket.s3-website-us-east-1.amazonaws.com`
- Backend: `http://your-ec2-ip/api`

---

## Prerequisites

### 1. AWS Account
- Go to https://aws.amazon.com
- Click "Create an AWS Account"
- Provide email and credit card
- **Free tier**: 750 hours/month of EC2 t2.micro (first 12 months)

### 2. AWS CLI (Optional but helpful)
```bash
pip install awscli
aws configure
```

### 3. Git Repository (Optional)
If you want to use Git for deployment:
```bash
git init
git add .
git commit -m "Initial commit"
```

---

## Part 1: Deploy Backend on EC2

### Step 1: Launch EC2 Instance

1. **Go to EC2 Console**
   - Open https://console.aws.amazon.com/ec2
   - Make sure you're in your preferred region (e.g., us-east-1)

2. **Click "Launch Instance"**

3. **Configure Instance**:

   **Name**: `vocabulary-backend`
   
   **Application and OS Images (AMI)**:
   - Choose: **Ubuntu Server 22.04 LTS**
   - Architecture: 64-bit (x86)
   
   **Instance type**:
   - Choose: **t2.micro** (Free tier eligible)
   - 1 vCPU, 1 GB RAM
   
   **Key pair (login)**:
   - Click "Create new key pair"
   - Name: `vocabulary-key`
   - Type: RSA
   - Format: .pem (for Mac/Linux) or .ppk (for Windows/PuTTY)
   - Click "Create key pair"
   - **IMPORTANT**: Save the .pem file - you can't download it again!
   
   **Network settings**:
   - Click "Edit"
   - **Security group name**: vocabulary-backend-sg
   - **Add rules**:
     - SSH (port 22) - Source: My IP (your current IP)
     - HTTP (port 80) - Source: Anywhere (0.0.0.0/0)
     - HTTPS (port 443) - Source: Anywhere (0.0.0.0/0)
     - Custom TCP (port 5001) - Source: Anywhere (0.0.0.0/0)
   
   **Configure storage**:
   - 8 GB gp3 (default is fine)
   
4. **Click "Launch instance"**

5. **Wait ~2 minutes** for instance to start

6. **Get your instance's public IP**:
   - Click on your instance
   - Copy "Public IPv4 address" (e.g., 54.123.45.67)

### Step 2: Connect to EC2

**On Mac/Linux**:
```bash
# Make key file secure (required)
chmod 400 ~/Downloads/vocabulary-key.pem

# Connect via SSH
ssh -i ~/Downloads/vocabulary-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

**On Windows** (using PuTTY):
1. Open PuTTY
2. Host Name: `ubuntu@YOUR_EC2_PUBLIC_IP`
3. Connection → SSH → Auth → Browse for your .ppk file
4. Click "Open"

**You should see**:
```
Welcome to Ubuntu 22.04 LTS
ubuntu@ip-172-31-xx-xx:~$
```

### Step 3: Install System Dependencies

```bash
# Update package list
sudo apt update

# Upgrade existing packages
sudo apt upgrade -y

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Nginx (web server)
sudo apt install nginx -y

# Install Git
sudo apt install git -y

# Verify installations
python3 --version  # Should show Python 3.10+
nginx -v           # Should show nginx version
```

### Step 4: Deploy Backend Code

**Option A: Using Git (Recommended)**

```bash
# Clone your repository
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/vocabulary-app.git
cd vocabulary-app/backend
```

**Option B: Upload Files Manually**

On your local machine:
```bash
# Compress backend folder
cd /path/to/your/project
tar -czf backend.tar.gz backend/

# Upload to EC2
scp -i ~/Downloads/vocabulary-key.pem backend.tar.gz ubuntu@YOUR_EC2_IP:/home/ubuntu/

# On EC2, extract
ssh -i ~/Downloads/vocabulary-key.pem ubuntu@YOUR_EC2_IP
cd /home/ubuntu
tar -xzf backend.tar.gz
cd backend
```

### Step 5: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt

# Install production dependencies
pip install -r requirements-prod.txt

# Verify installation
pip list
```

### Step 6: Initialize Database

```bash
# Create data directory
mkdir -p data

# Initialize database
python3 -c "from app.database import init_db; init_db()"

# Verify database was created
ls -lh data/
# Should see vocabulary.db
```

### Step 7: Test Backend Manually

```bash
# Test that Flask works
python3 run.py

# You should see:
# * Running on http://0.0.0.0:5001
```

Press `Ctrl+C` to stop.

### Step 8: Configure Gunicorn (Production Server)

Gunicorn is a production-grade WSGI server (better than Flask's built-in server).

**Create systemd service file**:

```bash
sudo nano /etc/systemd/system/vocabulary-backend.service
```

**Paste this content**:

```ini
[Unit]
Description=Vocabulary App Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/vocabulary-app/backend
Environment="PATH=/home/ubuntu/vocabulary-app/backend/venv/bin"
Environment="SECRET_KEY=CHANGE_THIS_TO_RANDOM_STRING"
Environment="CORS_ORIGINS=http://YOUR_S3_BUCKET_URL"
ExecStart=/home/ubuntu/vocabulary-app/backend/venv/bin/gunicorn \
    --workers 3 \
    --bind 0.0.0.0:5001 \
    --access-logfile /var/log/vocabulary-backend-access.log \
    --error-logfile /var/log/vocabulary-backend-error.log \
    app.app:app

Restart=always

[Install]
WantedBy=multi-user.target
```

**Generate a secret key**:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and replace `CHANGE_THIS_TO_RANDOM_STRING` in the service file.

**Save and exit**: `Ctrl+X`, then `Y`, then `Enter`

**Start the service**:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start the service
sudo systemctl start vocabulary-backend

# Enable auto-start on boot
sudo systemctl enable vocabulary-backend

# Check status
sudo systemctl status vocabulary-backend
```

**You should see**:
```
● vocabulary-backend.service - Vocabulary App Backend
   Active: active (running)
```

**Test it**:
```bash
curl http://localhost:5001/api/health
```

Should return: `{"status": "healthy"}`

### Step 9: Configure Nginx (Reverse Proxy)

Nginx will:
- Handle HTTP requests
- Forward API requests to Gunicorn
- Serve static files (if needed)
- Add security headers

**Create Nginx configuration**:

```bash
sudo nano /etc/nginx/sites-available/vocabulary-backend
```

**Paste this content**:

```nginx
server {
    listen 80;
    server_name YOUR_EC2_PUBLIC_IP;  # Replace with your EC2 IP

    # Increase upload size for CSV files
    client_max_body_size 10M;

    # API endpoints
    location /api {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers (if needed)
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
        add_header Access-Control-Allow-Headers "Content-Type, Authorization";
    }

    # Health check
    location /health {
        proxy_pass http://localhost:5001/api/health;
    }
}
```

Replace `YOUR_EC2_PUBLIC_IP` with your actual IP.

**Save and exit**: `Ctrl+X`, then `Y`, then `Enter`

**Enable the site**:

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/vocabulary-backend /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Should show: syntax is ok, test is successful

# Restart Nginx
sudo systemctl restart nginx

# Check status
sudo systemctl status nginx
```

### Step 10: Test Backend from Internet

On your local machine:

```bash
# Replace with your EC2 IP
curl http://YOUR_EC2_IP/api/health
```

Should return: `{"status": "healthy"}`

**If it doesn't work**:
1. Check security group allows port 80
2. Check Nginx is running: `sudo systemctl status nginx`
3. Check Gunicorn is running: `sudo systemctl status vocabulary-backend`
4. Check logs: `sudo tail -f /var/log/vocabulary-backend-error.log`

---

## Part 2: Deploy Frontend on S3

### Step 1: Build Frontend for Production

On your local machine:

```bash
cd frontend

# Create production environment file
cat > .env.production << EOF
VITE_API_URL=http://YOUR_EC2_IP/api
EOF

# Replace YOUR_EC2_IP with your actual EC2 public IP

# Install dependencies (if not already done)
npm install

# Build for production
npm run build
```

This creates `frontend/dist/` folder with optimized files.

### Step 2: Create S3 Bucket

1. **Go to S3 Console**
   - Open https://console.aws.amazon.com/s3

2. **Click "Create bucket"**

3. **Configure bucket**:
   
   **Bucket name**: `vocabulary-app-frontend-YOUR_NAME`
   - Must be globally unique
   - Use lowercase, numbers, hyphens only
   - Example: `vocabulary-app-frontend-john`
   
   **AWS Region**: `us-east-1` (or your preferred region)
   
   **Object Ownership**: ACLs disabled (recommended)
   
   **Block Public Access settings**:
   - **UNCHECK** "Block all public access"
   - Check the acknowledgment box
   
   **Bucket Versioning**: Disabled (or enable if you want)
   
   **Tags**: (optional)
   
   **Default encryption**: Enable (Server-side encryption with Amazon S3 managed keys)

4. **Click "Create bucket"**

### Step 3: Upload Frontend Files

**Option A: Using AWS Console (Easy)**

1. Click on your bucket name
2. Click "Upload"
3. Click "Add files" and "Add folder"
4. Select all files from `frontend/dist/` folder
5. Click "Upload"
6. Wait for upload to complete

**Option B: Using AWS CLI (Faster)**

```bash
# Configure AWS CLI (if not done)
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-east-1
# Default output format: json

# Upload files
cd frontend/dist
aws s3 sync . s3://vocabulary-app-frontend-YOUR_NAME --acl public-read

# You should see files being uploaded
```

### Step 4: Enable Static Website Hosting

1. **Go to your S3 bucket**
2. **Click "Properties" tab**
3. **Scroll down to "Static website hosting"**
4. **Click "Edit"**
5. **Configure**:
   - Static website hosting: **Enable**
   - Hosting type: **Host a static website**
   - Index document: `index.html`
   - Error document: `index.html` (important for React Router!)
6. **Click "Save changes"**

7. **Copy the "Bucket website endpoint"**
   - Example: `http://vocabulary-app-frontend-john.s3-website-us-east-1.amazonaws.com`

### Step 5: Configure Bucket Policy (Make Public)

1. **Click "Permissions" tab**
2. **Scroll to "Bucket policy"**
3. **Click "Edit"**
4. **Paste this policy**:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::vocabulary-app-frontend-YOUR_NAME/*"
    }
  ]
}
```

**Replace** `vocabulary-app-frontend-YOUR_NAME` with your actual bucket name.

5. **Click "Save changes"**

### Step 6: Update Backend CORS

Your backend needs to allow requests from your S3 website.

**On EC2**:

```bash
# Edit the systemd service file
sudo nano /etc/systemd/system/vocabulary-backend.service

# Update the CORS_ORIGINS line:
Environment="CORS_ORIGINS=http://vocabulary-app-frontend-YOUR_NAME.s3-website-us-east-1.amazonaws.com"

# Save and exit

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart vocabulary-backend
```

### Step 7: Test Your App!

1. **Open your S3 website URL** in a browser:
   ```
   http://vocabulary-app-frontend-YOUR_NAME.s3-website-us-east-1.amazonaws.com
   ```

2. **You should see the login page**

3. **Register a new account**

4. **Test all features**:
   - Add vocabulary entries
   - Search
   - Edit/delete entries
   - Import CSV
   - Export CSV

---

## Part 3: Optional Enhancements

### Add Custom Domain (Optional)

1. **Buy a domain** (Route 53, GoDaddy, Namecheap, etc.)
2. **Create CloudFront distribution** (for HTTPS)
3. **Point domain to CloudFront**
4. **Update CORS settings**

### Add HTTPS (Recommended for Production)

1. **Get SSL certificate** (AWS Certificate Manager - free!)
2. **Create CloudFront distribution**
3. **Configure CloudFront to use S3 as origin**
4. **Update frontend to use CloudFront URL**

### Upgrade Database to RDS (For Multiple Users)

1. **Create RDS PostgreSQL instance**
2. **Migrate data from SQLite**
3. **Update backend configuration**

---

## Maintenance & Updates

### Update Backend Code

```bash
# SSH to EC2
ssh -i ~/Downloads/vocabulary-key.pem ubuntu@YOUR_EC2_IP

# Pull latest code
cd /home/ubuntu/vocabulary-app/backend
git pull

# Restart service
sudo systemctl restart vocabulary-backend
```

### Update Frontend Code

```bash
# On local machine
cd frontend
npm run build

# Upload to S3
cd dist
aws s3 sync . s3://vocabulary-app-frontend-YOUR_NAME --acl public-read --delete
```

### View Logs

```bash
# Backend logs
sudo tail -f /var/log/vocabulary-backend-error.log
sudo tail -f /var/log/vocabulary-backend-access.log

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Systemd logs
sudo journalctl -u vocabulary-backend -f
```

### Backup Database

```bash
# On EC2
cd /home/ubuntu/vocabulary-app/backend/data
cp vocabulary.db vocabulary.db.backup-$(date +%Y%m%d)

# Download to local machine
scp -i ~/Downloads/vocabulary-key.pem ubuntu@YOUR_EC2_IP:/home/ubuntu/vocabulary-app/backend/data/vocabulary.db ./vocabulary-backup.db
```

---

## Troubleshooting

### Backend not responding

```bash
# Check if Gunicorn is running
sudo systemctl status vocabulary-backend

# Check logs
sudo journalctl -u vocabulary-backend -n 50

# Restart service
sudo systemctl restart vocabulary-backend
```

### Frontend shows blank page

1. Check browser console for errors (F12)
2. Verify API URL in `.env.production`
3. Check CORS settings on backend
4. Verify S3 bucket policy is public

### CORS errors

1. Update CORS_ORIGINS in systemd service file
2. Restart backend: `sudo systemctl restart vocabulary-backend`
3. Clear browser cache

### Can't SSH to EC2

1. Check security group allows SSH from your IP
2. Verify key file permissions: `chmod 400 vocabulary-key.pem`
3. Check instance is running in EC2 console

---

## Cost Breakdown

### EC2 t2.micro
- **Free tier**: 750 hours/month (first 12 months)
- **After free tier**: ~$8/month

### S3 Storage
- **First 5 GB**: Free
- **After**: $0.023/GB/month
- **Typical**: $0.50-2/month

### Data Transfer
- **First 1 GB out**: Free
- **After**: $0.09/GB
- **Typical**: $1-5/month

### Total Estimated Cost
- **First year**: $0-5/month (free tier)
- **After first year**: $10-15/month

---

## Security Checklist

- [ ] Changed SECRET_KEY to random string
- [ ] Restricted SSH access to your IP only
- [ ] Enabled HTTPS (CloudFront + ACM)
- [ ] Regular backups of database
- [ ] Updated packages regularly
- [ ] Monitoring enabled (CloudWatch)
- [ ] Strong passwords for user accounts

---

## Next Steps

1. ✅ Backend deployed on EC2
2. ✅ Frontend deployed on S3
3. ✅ App is live and accessible
4. 🔄 Optional: Add custom domain
5. 🔄 Optional: Add HTTPS
6. 🔄 Optional: Upgrade to RDS

**Your app is now live on AWS!** 🎉

Share your S3 URL with friends and start using your vocabulary app from anywhere!
