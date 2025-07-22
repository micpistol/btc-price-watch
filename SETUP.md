# BTC Price Watchdog - Setup Guide

This guide will help you deploy your own instance of the BTC Price Watchdog service on Fly.io.

## Prerequisites

1. **Fly.io Account**: Sign up at [fly.io](https://fly.io)
2. **GitHub Account**: For repository hosting and CI/CD
3. **Basic familiarity with command line tools**

## Step 1: Fork and Clone the Repository

1. **Fork this repository** to your GitHub account
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/btc-price-watchdog.git
   cd btc-price-watchdog
   ```

## Step 2: Install Fly.io CLI

```bash
# macOS (using Homebrew)
brew install flyctl

# Linux/macOS (using install script)
curl -L https://fly.io/install.sh | sh

# Windows (using PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

## Step 3: Authenticate with Fly.io

```bash
fly auth login
```

Follow the browser prompts to authenticate your account.

## Step 4: Create Your Fly.io App

```bash
# Create a new app (replace 'your-app-name' with your desired name)
fly apps create your-app-name --org personal

# Or use the automated deployment script
./deploy.sh
```

## Step 5: Set Up GitHub Secrets (Optional - for CI/CD)

If you want automatic deployments on code pushes:

1. **Get your Fly.io API token**:
   ```bash
   fly tokens create deploy
   ```

2. **Add the token to GitHub Secrets**:
   - Go to your GitHub repository
   - Navigate to Settings → Secrets and variables → Actions
   - Create a new secret named `FLY_API_TOKEN`
   - Paste your API token

## Step 6: Deploy Your Service

### Option A: Manual Deployment
```bash
fly deploy
```

### Option B: Using the Deployment Script
```bash
./deploy.sh
```

## Step 7: Verify Your Deployment

1. **Check app status**:
   ```bash
   fly status
   ```

2. **Test the health endpoint**:
   ```bash
   curl https://your-app-name.fly.dev/health
   ```

3. **Test the main API**:
   ```bash
   curl https://your-app-name.fly.dev/
   ```

## Configuration

The service uses environment variables for configuration. These are set in the `fly.toml` file:

- `COINBASE_WS_URL`: Coinbase WebSocket URL (default: wss://ws-feed.exchange.coinbase.com)
- `DB_PATH`: Database file path (default: /data/btc_price_history.db)
- `HEARTBEAT_PATH`: Heartbeat file path (default: /data/btc_logger_heartbeat.txt)
- `LOG_PATH`: Log file path (default: /data/btc_price_log.txt)
- `TIMEZONE`: Timezone for timestamps (default: America/New_York)

## Customization

### Changing the App Name

1. **Update fly.toml**:
   ```toml
   app = 'your-new-app-name'
   ```

2. **Update deployment script** (if using):
   ```bash
   # Edit deploy.sh and change 'btc-watchdog' to your app name
   ```

### Adding Custom Endpoints

1. **Edit app.py** to add new API endpoints
2. **Update the root endpoint** documentation
3. **Deploy changes**:
   ```bash
   fly deploy
   ```

## Monitoring and Maintenance

### View Logs
```bash
fly logs
```

### SSH into the Machine
```bash
fly ssh console
```

### Monitor Price Logger
```bash
fly ssh console -C 'tail -f /data/btc_price_log.txt'
```

### Check Database
```bash
fly ssh console -C 'sqlite3 /data/btc_price_history.db "SELECT COUNT(*) FROM price_log;"'
```

## Troubleshooting

### Common Issues

1. **App won't start**:
   - Check logs: `fly logs`
   - Verify environment variables in `fly.toml`

2. **Database issues**:
   - Check volume mount: `fly volumes list`
   - Verify volume exists and is attached

3. **WebSocket connection issues**:
   - Check Coinbase API status
   - Verify network connectivity

### Getting Help

- Check the [Fly.io documentation](https://fly.io/docs/)
- Review the [README.md](README.md) for API documentation
- Check the [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment info

## Security Considerations

- The service uses public Coinbase WebSocket API (no authentication required)
- Database is stored in Fly.io volumes (encrypted at rest)
- No sensitive data is stored in the codebase
- All API endpoints are public (consider adding authentication if needed)

## Cost Optimization

- The service runs on Fly.io's free tier (3 shared-cpu-1x 256mb VMs)
- Database storage is minimal (SQLite with price data)
- Consider scaling down during low-usage periods

## Next Steps

Once your service is running:

1. **Test all API endpoints** to ensure they work correctly
2. **Set up monitoring** (optional: add uptime monitoring)
3. **Customize the frontend** (dashboard.html, mobile-dashboard.html)
4. **Add additional features** as needed

Your BTC Price Watchdog service is now ready to use! 🚀 