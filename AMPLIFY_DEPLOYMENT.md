# AWS Amplify Deployment Guide - Complete Walkthrough

Deploy your vocabulary app to AWS Amplify in under 30 minutes!

---

## What is AWS Amplify?

Amplify is AWS's easiest deployment platform. It automatically handles:
- ✅ Frontend hosting (React app on CloudFront CDN)
- ✅ Backend hosting (Flask API)
- ✅ SSL certificates (HTTPS)
- ✅ Custom domains
- ✅ Automatic deployments from Git
- ✅ Build process
- ✅ Environment variables

**You just push to GitHub, Amplify does the rest!**

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              AWS Amplify (Managed)                   │
│                                                      │
│  ┌──────────────────┐      ┌──────────────────┐   │
│  │   Frontend       │      │    Backend       │   │
│  │   React App      │◄────►│    Flask API     │   │
│  │   CloudFront CDN │      │    Container     │   │
│  └──────────────────┘      └──────────────────┘   │
│                                     │               │
│                                     ▼               │
│                            ┌──────────────────┐   │
│                            │   SQLite DB      │   │
│                            │   (Persistent)   │   │
│                            └──────────────────┘   │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
         https://main.d1234abcd.amplifyapp.com
```

---

## Prerequisites

### 1. AWS Account
- Go to https://aws.amazon.com
- Click "Create an AWS Account"
- Provide email and credit card
- **Free tier**: Generous limits for 12 months

### 2. GitHub Account
- Go to https://github.com
- Create account if you don't have one
- Free for public repositories

### 3. Git Installed
```bash
git --version
# If not installed: brew install git (Mac) or download from git-scm.com
```

---

## Step 1: Prepare Your Code for Amplify

I'll create the necessary configuration files for you.

### Files We Need to Create:

1. `amplify.yml` - Build configuration
2. `backend/Dockerfile` - Container for Flask
3. `.gitignore` - Files to exclude from Git
4. `frontend/.env.production` - Production environment variables

Let me create these for you...


✅ **Done!** I've created all necessary files:
- `amplify.yml` - Amplify build configuration
- `backend/Dockerfile` - Docker container for Flask
- `backend/requirements-prod.txt` - Production dependencies
- `frontend/.env.production` - Production environment variables

---

## Step 2: Push Your Code to GitHub

### Option A: Create New Repository on GitHub

1. **Go to GitHub**: https://github.com
2. **Click** the "+" icon → "New repository"
3. **Configure**:
   - Repository name: `vocabulary-app`
   - Description: "Vocabulary visualization web app"
   - Visibility: Public (or Private if you prefer)
   - **Don't** initialize with README (we already have code)
4. **Click** "Create repository"

### Option B: Initialize Git Locally

```bash
# Navigate to your project
cd /Users/vggnanas/Documents/kiro-projects/words

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Vocabulary app ready for Amplify"

# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/vocabulary-app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Enter your GitHub credentials when prompted.**

---

## Step 3: Deploy with AWS Amplify

### 3.1 Go to Amplify Console

1. **Open AWS Console**: https://console.aws.amazon.com
2. **Search for** "Amplify" in the search bar
3. **Click** "AWS Amplify"
4. **Click** "Get started" under "Amplify Hosting"

### 3.2 Connect Your Repository

1. **Choose** "GitHub"
2. **Click** "Continue"
3. **Authorize AWS Amplify** (if first time)
   - GitHub will ask for permission
   - Click "Authorize aws-amplify-console"
4. **Select your repository**: `vocabulary-app`
5. **Select branch**: `main`
6. **Click** "Next"

### 3.3 Configure Build Settings

Amplify will auto-detect your `amplify.yml` file.

**App name**: `vocabulary-app` (or your preferred name)

**Build settings**: Should show your `amplify.yml` content

**Advanced settings** (click to expand):
- **Environment variables** (we'll add these later)
- **Build image**: Default (Amazon Linux 2)

**Click** "Next"

### 3.4 Review and Deploy

1. **Review** all settings
2. **Click** "Save and deploy"

**Amplify will now**:
1. Provision resources (~2 minutes)
2. Build frontend (~3 minutes)
3. Build backend (~5 minutes)
4. Deploy (~2 minutes)

**Total time**: ~10-15 minutes

☕ **Grab a coffee!** Watch the build logs in real-time.

---

## Step 4: Configure Environment Variables

While the build is running (or after it completes):

### 4.1 Generate Secret Key

On your local machine:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output (looks like: `a1b2c3d4e5f6...`)

### 4.2 Add Environment Variables

1. **In Amplify Console**, click your app name
2. **Click** "App settings" → "Environment variables"
3. **Click** "Manage variables"
4. **Add these variables**:

| Variable | Value | Example |
|----------|-------|---------|
| `SECRET_KEY` | Your generated key | `a1b2c3d4e5f6...` |
| `CORS_ORIGINS` | Your Amplify URL | `https://main.d1234.amplifyapp.com` |
| `SESSION_DURATION_HOURS` | `24` | `24` |

5. **Click** "Save"

### 4.3 Get Your Amplify URL

1. **Wait for deployment** to complete (green checkmark)
2. **Copy your URL**: `https://main.d1234abcd.amplifyapp.com`
3. **Update CORS_ORIGINS**:
   - Go back to Environment variables
   - Update `CORS_ORIGINS` with your actual URL
   - Save

### 4.4 Redeploy

1. **Click** "Redeploy this version" (top right)
2. **Wait** ~5 minutes for rebuild

---

## Step 5: Test Your App!

### 5.1 Open Your App

Click on your Amplify URL: `https://main.d1234abcd.amplifyapp.com`

You should see your login page! 🎉

### 5.2 Test All Features

1. **Register** a new account
   - Username: `testuser`
   - Password: `password123`

2. **Add vocabulary entries**
   - Word: "serendipity"
   - Meaning: "finding something good without looking for it"

3. **Search** for entries

4. **Import CSV**
   - Use the `sample_vocabulary.csv` file

5. **Export CSV**
   - Download your vocabulary

6. **Edit and delete** entries

**Everything should work!**

---

## Step 6: Set Up Automatic Deployments

Now every time you push to GitHub, Amplify automatically deploys!

### Test It:

```bash
# Make a small change
echo "# Deployed with Amplify" >> README.md

# Commit and push
git add .
git commit -m "Test automatic deployment"
git push

# Go to Amplify Console
# Watch it automatically build and deploy!
```

**Deployment time**: ~5-10 minutes per push

---

## Step 7: Add Custom Domain (Optional)

### 7.1 Buy a Domain

Buy from:
- **AWS Route 53**: https://console.aws.amazon.com/route53
- **GoDaddy**: https://godaddy.com
- **Namecheap**: https://namecheap.com
- **Google Domains**: https://domains.google

Example: `myvocab.com` ($10-15/year)

### 7.2 Add Domain to Amplify

1. **In Amplify Console**, click "Domain management"
2. **Click** "Add domain"
3. **Enter your domain**: `myvocab.com`
4. **Configure subdomains**:
   - `www.myvocab.com` → Redirect to `myvocab.com`
   - `myvocab.com` → Main app
5. **Click** "Save"

### 7.3 Update DNS

Amplify will show you DNS records to add:

**If using Route 53** (easiest):
- Amplify does it automatically!

**If using other registrar**:
1. Go to your domain registrar
2. Add the CNAME records Amplify provides
3. Wait 15-60 minutes for DNS propagation

### 7.4 SSL Certificate

Amplify automatically:
- Requests SSL certificate from AWS Certificate Manager
- Configures HTTPS
- Redirects HTTP to HTTPS

**Wait ~15 minutes**, then access: `https://myvocab.com`

---

## Monitoring and Logs

### View Build Logs

1. **In Amplify Console**, click your app
2. **Click** on a deployment
3. **View logs** for each phase:
   - Provision
   - Build (frontend)
   - Build (backend)
   - Deploy

### View Application Logs

1. **Click** "Monitoring"
2. **View**:
   - Request count
   - Error rate
   - Latency
   - Data transfer

### Access Logs

1. **Click** "Access logs"
2. **Enable** access logging
3. **View** in CloudWatch Logs

---

## Updating Your App

### Update Code

```bash
# Make changes to your code
# ... edit files ...

# Commit and push
git add .
git commit -m "Add new feature"
git push

# Amplify automatically deploys!
```

### Update Environment Variables

1. **Go to** App settings → Environment variables
2. **Update** values
3. **Click** "Save"
4. **Redeploy** (Amplify → Redeploy this version)

### Rollback to Previous Version

1. **Go to** your app in Amplify
2. **Click** on a previous successful deployment
3. **Click** "Redeploy this version"

---

## Troubleshooting

### Build Failed

**Check build logs**:
1. Click on the failed deployment
2. Expand each phase to see errors
3. Common issues:
   - Missing dependencies in `requirements-prod.txt`
   - Syntax errors in code
   - Wrong Node.js version

**Fix**:
```bash
# Fix the issue locally
# Test locally first
npm run build  # Test frontend
python run.py  # Test backend

# Push fix
git add .
git commit -m "Fix build issue"
git push
```

### Frontend Shows Blank Page

**Check browser console** (F12):
- Look for errors
- Check if API calls are failing

**Common fixes**:
1. Update `CORS_ORIGINS` environment variable
2. Check backend is running (visit `/api/health`)
3. Clear browser cache

### Backend Not Responding

**Check**:
1. Backend build succeeded (green checkmark)
2. Environment variables are set
3. CORS_ORIGINS matches your frontend URL

**View backend logs**:
1. Amplify Console → Monitoring
2. Click "View logs in CloudWatch"

### CORS Errors

**Error**: `Access to fetch at '...' has been blocked by CORS policy`

**Fix**:
1. Go to Environment variables
2. Update `CORS_ORIGINS` to your exact Amplify URL
3. Include `https://` and no trailing slash
4. Redeploy

---

## Cost Breakdown

### AWS Amplify Pricing

**Build minutes**:
- First 1,000 minutes/month: **FREE**
- After: $0.01/minute
- Typical: 10 builds/month × 10 min = 100 minutes = **FREE**

**Hosting**:
- Storage: $0.023/GB/month
- Data transfer: $0.15/GB served
- Typical: 1 GB storage + 5 GB transfer = **$1/month**

**Total estimated cost**: **$1-5/month**

### Free Tier (First 12 Months)

- 1,000 build minutes/month
- 15 GB data transfer/month
- 5 GB storage

**Most personal projects stay in free tier!**

---

## Comparison: Amplify vs EC2

| Feature | Amplify | EC2 + S3 |
|---------|---------|----------|
| **Setup time** | 30 minutes | 2 hours |
| **Difficulty** | Easy | Medium |
| **Cost** | $1-5/month | $10-30/month |
| **Maintenance** | None | Manual updates |
| **Scaling** | Automatic | Manual |
| **HTTPS** | Automatic | Manual setup |
| **Deployments** | Automatic | Manual |
| **Monitoring** | Built-in | Setup required |
| **Best for** | Quick deployment | Learning AWS |

---

## Advanced Features

### Branch Deployments

Deploy different branches to different URLs:

1. **Main branch**: `https://main.d1234.amplifyapp.com` (production)
2. **Dev branch**: `https://dev.d1234.amplifyapp.com` (testing)

**Setup**:
1. Create `dev` branch: `git checkout -b dev`
2. Push: `git push origin dev`
3. In Amplify, connect the `dev` branch
4. Each branch deploys independently!

### Preview Deployments

Get a unique URL for each pull request:

1. **Enable** in Amplify settings
2. **Create** pull request on GitHub
3. **Amplify** automatically creates preview URL
4. **Test** changes before merging

### Password Protection

Protect your app with password:

1. **Go to** App settings → Access control
2. **Enable** access control
3. **Set** username and password
4. **Save**

Now visitors need password to access your app!

---

## Database Considerations

### Current Setup: SQLite

**Pros**:
- Simple, no extra cost
- Works immediately
- Good for personal use

**Cons**:
- Data resets on each deployment
- Not suitable for multiple users
- No backups

### Upgrade to RDS (Recommended for Production)

**When to upgrade**:
- Multiple users
- Need data persistence
- Want automatic backups

**Setup**:
1. Create RDS PostgreSQL instance
2. Add `DATABASE_URL` environment variable
3. Update `requirements-prod.txt` (add `psycopg2-binary`)
4. Redeploy

**Cost**: ~$15-30/month

---

## Security Best Practices

### ✅ Already Configured

- HTTPS (automatic)
- Environment variables (secrets not in code)
- CORS protection
- Password hashing (bcrypt)

### 🔒 Additional Security

1. **Enable WAF** (Web Application Firewall)
   - Amplify → App settings → Security
   - Protects against common attacks

2. **Set up monitoring alerts**
   - CloudWatch alarms for errors
   - Email notifications

3. **Regular updates**
   - Update dependencies monthly
   - Check for security vulnerabilities

4. **Backup database**
   - If using RDS: automatic backups
   - If using SQLite: manual backups

---

## Next Steps

### ✅ You've Deployed!

Your app is now live at: `https://main.d1234abcd.amplifyapp.com`

### 🚀 What's Next?

1. **Share with friends** - Get feedback!
2. **Add custom domain** - Make it professional
3. **Monitor usage** - Check Amplify dashboard
4. **Add features** - Word cloud, card view, etc.
5. **Upgrade database** - Move to RDS when needed

### 📚 Learn More

- **Amplify Docs**: https://docs.amplify.aws
- **AWS Free Tier**: https://aws.amazon.com/free
- **Amplify Discord**: https://discord.gg/amplify

---

## Summary

**What you accomplished**:
- ✅ Deployed full-stack app to AWS
- ✅ Automatic HTTPS
- ✅ Automatic deployments from GitHub
- ✅ Professional hosting
- ✅ Monitoring and logs
- ✅ Scalable infrastructure

**Total time**: ~30 minutes
**Total cost**: $1-5/month
**Difficulty**: Easy

**Congratulations! Your vocabulary app is live on AWS! 🎉**

---

## Quick Reference

### Useful Commands

```bash
# Push updates
git add .
git commit -m "Update message"
git push

# View logs
# Go to Amplify Console → Click deployment → View logs

# Rollback
# Amplify Console → Previous deployment → Redeploy
```

### Useful Links

- **Amplify Console**: https://console.aws.amazon.com/amplify
- **Your App**: https://main.d1234abcd.amplifyapp.com
- **GitHub Repo**: https://github.com/YOUR_USERNAME/vocabulary-app
- **AWS Support**: https://console.aws.amazon.com/support

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Session encryption |
| `CORS_ORIGINS` | Frontend URL |
| `SESSION_DURATION_HOURS` | Session timeout |

---

**Need help?** Check the troubleshooting section or ask me!
