#!/bin/bash

# BTC Price Watchdog Deployment Script for Fly.io
# This script automates the deployment process

set -e

echo "🚀 Starting BTC Price Watchdog deployment to Fly.io..."

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
if ! fly apps list | grep -q "btc-watchdog"; then
    echo "🆕 Creating new Fly.io app: btc-watchdog"
    fly apps create btc-watchdog --org personal
else
    echo "✅ App btc-watchdog already exists"
fi

# Create persistent volume if it doesn't exist
echo "💾 Checking for persistent volume..."
if ! fly volumes list | grep -q "btc_data"; then
    echo "🆕 Creating persistent volume: btc_data"
    fly volumes create btc_data --size 1 --region ord
else
    echo "✅ Volume btc_data already exists"
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
echo "   https://btc-watchdog.fly.dev"
echo ""
echo "📊 API Endpoints:"
echo "   - Health check: https://btc-watchdog.fly.dev/health"
echo "   - Latest price: https://btc-watchdog.fly.dev/latest"
echo "   - Price history: https://btc-watchdog.fly.dev/prices"
echo "   - Statistics: https://btc-watchdog.fly.dev/stats"
echo ""
echo "📝 To view logs:"
echo "   fly logs"
echo ""
echo "🔧 To SSH into the machine:"
echo "   fly ssh console"
echo ""
echo "📈 To monitor the price logger:"
echo "   fly ssh console -C 'tail -f /data/btc_price_log.txt'" 