# 🚀 Deployment Guide: From GitHub to Fly.io

This guide shows you how to deploy your BTC Price Watchdog service from a GitHub repository to Fly.io.

## 📋 Prerequisites

1. **Fly.io Account** with payment information added
2. **GitHub Account**
3. **Fly CLI** installed and authenticated

## 🚀 Method 1: Manual Deployment from GitHub

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `btc-price-watchdog` (or your preferred name)
3. Make it public or private
4. **Don't** initialize with README, .gitignore, or license

### Step 2: Push Your Code

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/btc-price-watchdog.git

# Push to GitHub
git push -u origin master
```

### Step 3: Deploy from GitHub

```bash
# Set up Fly CLI
export FLYCTL_INSTALL="/Users/michael/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"

# Deploy from GitHub repository
fly launch --name btc-watchdog --region ord --source https://github.com/YOUR_USERNAME/btc-price-watchdog.git
```

### Step 4: Create Persistent Volume

```bash
# Create persistent volume for database
fly volumes create btc_data --size 1 --region ord
```

### Step 5: Deploy

```bash
# Deploy the application
fly deploy
```

## 🤖 Method 2: Automated Deployment with GitHub Actions

### Step 1: Set Up GitHub Repository

1. Push your code to GitHub (same as Method 1, Step 2)
2. The GitHub Actions workflow is already included in this repository

### Step 2: Get Fly.io API Token

```bash
# Generate API token
fly tokens create deploy

# Copy the token (you'll need it for GitHub)
```

### Step 3: Add Secret to GitHub

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `FLY_API_TOKEN`
5. Value: Paste your Fly.io API token

### Step 4: Deploy

```bash
# Initial deployment (creates the app)
fly launch --name btc-watchdog --region ord --source https://github.com/YOUR_USERNAME/btc-price-watchdog.git

# Create persistent volume
fly volumes create btc_data --size 1 --region ord

# Deploy
fly deploy
```

### Step 5: Automated Deployments

Now every time you push to the `master` branch, GitHub Actions will automatically deploy your app!

## 🚀 Method 3: One-Click Deploy with Fly.io

### Step 1: Prepare Your Repository

Make sure your repository has:
- ✅ `Dockerfile`
- ✅ `fly.toml`
- ✅ `requirements.txt`
- ✅ All source code

### Step 2: Deploy Button

Add this button to your README.md:

```markdown
[![Deploy to Fly.io](https://fly.io/button.svg)](https://fly.io/apps/new?name=btc-watchdog&region=ord&source=https://github.com/YOUR_USERNAME/btc-price-watchdog)
```

### Step 3: Click and Deploy

1. Click the "Deploy to Fly.io" button
2. Log in to Fly.io
3. Follow the setup wizard
4. Your app will be deployed automatically!

## 🔧 Configuration

### Environment Variables

The service uses these environment variables (already configured in `fly.toml`):

```toml
[env]
  DB_PATH = "/data/btc_price_history.db"
  LOG_PATH = "/data/btc_price_log.txt"
  HEARTBEAT_PATH = "/data/btc_logger_heartbeat.txt"
  COINBASE_WS_URL = "wss://ws-feed.exchange.coinbase.com"
  TIMEZONE = "America/New_York"
```

### Custom Configuration

To override settings:

```bash
# Set custom environment variables
fly secrets set CUSTOM_VAR=value

# Update configuration
fly deploy
```

## 📊 Monitoring Your Deployment

### Check Status

```bash
# View app status
fly status

# View logs
fly logs

# Check health
curl https://btc-watchdog.fly.dev/health
```

### SSH into Machine

```bash
# SSH into the running machine
fly ssh console

# Monitor price logger
fly ssh console -C "tail -f /data/btc_price_log.txt"

# Check database
fly ssh console -C "sqlite3 /data/btc_price_history.db 'SELECT COUNT(*) FROM price_log'"
```

### Scaling

```bash
# Scale to multiple instances
fly scale count 2

# Change VM size
fly scale vm shared-cpu-2x
```

## 🆘 Troubleshooting

### Common Issues

1. **Payment Required**
   - Add credit card to Fly.io account
   - Visit: https://fly.io/dashboard/billing

2. **Deployment Fails**
   - Check logs: `fly logs`
   - Verify Dockerfile syntax
   - Check requirements.txt

3. **App Not Starting**
   - Check health endpoint
   - View logs: `fly logs`
   - SSH into machine: `fly ssh console`

4. **Database Issues**
   - Verify volume mount: `fly ssh console -C "ls -la /data"`
   - Check database: `fly ssh console -C "sqlite3 /data/btc_price_history.db .tables"`

### Getting Help

- **Fly.io Docs**: https://fly.io/docs/
- **GitHub Issues**: Create issue in your repository
- **Fly.io Community**: https://community.fly.io/

## 🎉 Success!

Once deployed, your service will be available at:
- **API Base URL**: `https://btc-watchdog.fly.dev`
- **Health Check**: `https://btc-watchdog.fly.dev/health`
- **Latest Price**: `https://btc-watchdog.fly.dev/latest`
- **Price History**: `https://btc-watchdog.fly.dev/prices`
- **Statistics**: `https://btc-watchdog.fly.dev/stats`

Your BTC price watchdog will run 24/7 in the cloud! 🚀 