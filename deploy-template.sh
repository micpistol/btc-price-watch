#!/bin/bash

# BTC Price Watchdog Deployment Template
# Customize this script for your own deployment

set -e

# Configuration - CHANGE THESE VALUES
APP_NAME="your-btc-watchdog-app-name"
VOLUME_NAME="btc_data"
REGION="lax"  # Change to your preferred region

echo "🚀 Starting BTC Price Watchdog deployment to Fly.io..."
echo "📋 App Name: $APP_NAME"
echo "🌍 Region: $REGION"

# Check if fly CLI is installed
if ! command -v fly &> /dev/null; then
    echo "❌ Fly CLI not found. Installing..."
    curl -L https://fly.io/install.sh | sh
    export PATH="$HOME/.fly/bin:$PATH"
fi

# Check if we're logged in to Fly.io
if ! fly auth whoami &> /dev/null; then
    echo "❌ Not logged in to Fly.io. Please run 'fly auth login' first."
    exit 1
fi

# Create the app if it doesn't exist
echo "📋 Checking if app exists..."
if ! fly apps list | grep -q "$APP_NAME"; then
    echo "🆕 Creating new Fly.io app: $APP_NAME"
    fly apps create $APP_NAME --org personal
else
    echo "✅ App $APP_NAME already exists"
fi

# Create persistent volume if it doesn't exist
echo "💾 Checking for persistent volume..."
if ! fly volumes list | grep -q "$VOLUME_NAME"; then
    echo "🆕 Creating persistent volume: $VOLUME_NAME"
    fly volumes create $VOLUME_NAME --size 1 --region $REGION
else
    echo "✅ Volume $VOLUME_NAME already exists"
fi

# Deploy the application
echo "🚀 Deploying application..."
fly deploy

# Check deployment status
echo "🔍 Checking deployment status..."
fly status

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your BTC Price Watchdog API is now available at:"
echo "   https://$APP_NAME.fly.dev"
echo ""
echo "📊 API Endpoints:"
echo "   - Health check: https://$APP_NAME.fly.dev/health"
echo "   - Latest price: https://$APP_NAME.fly.dev/latest"
echo "   - Price history: https://$APP_NAME.fly.dev/prices"
echo "   - Statistics: https://$APP_NAME.fly.dev/stats"
echo ""
echo "📝 To view logs:"
echo "   fly logs"
echo ""
echo "🔧 To SSH into the machine:"
echo "   fly ssh console"
echo ""
echo "📈 To monitor the price logger:"
echo "   fly ssh console -C 'tail -f /data/btc_price_log.txt'"
echo ""
echo "🎉 Your BTC Price Watchdog service is ready!" 