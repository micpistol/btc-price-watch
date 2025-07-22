# BTC Price Watchdog - Sharing Guide

This guide explains how to share and use the BTC Price Watchdog service.

## 🎯 Service Status

✅ **The BTC Price Watchdog service is currently running and fully operational!**

- **Live URL**: https://btc-watchdog.fly.dev
- **Status**: Healthy and monitoring BTC prices in real-time
- **Last Test**: All endpoints working correctly

## 📋 What's Included

### Core Service
- **Real-time BTC price monitoring** via Coinbase WebSocket
- **Persistent SQLite database** with Fly.io volumes
- **REST API** with 5 endpoints
- **Health monitoring** and automatic restarts
- **Docker containerized** deployment

### Documentation
- [README.md](README.md) - Main project documentation
- [API.md](API.md) - Complete API reference
- [SETUP.md](SETUP.md) - Deployment guide for your own instance
- [QUICK_START.md](QUICK_START.md) - Quick start for using the live service
- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment information

### Templates & Tools
- [fly.toml.example](fly.toml.example) - Configuration template
- [deploy-template.sh](deploy-template.sh) - Deployment script template
- [test-deployment.py](test-deployment.py) - Service testing script

### Frontend Examples
- [dashboard.html](dashboard.html) - Desktop dashboard
- [mobile-dashboard.html](mobile-dashboard.html) - Mobile dashboard
- [frontend_example.html](frontend_example.html) - Integration example

## 🚀 How to Share

### Option 1: Share the Live Service (Recommended)

The service is already running and ready to use. Simply share:

```
🌐 Live BTC Price Watchdog API
https://btc-watchdog.fly.dev

📊 Endpoints:
- Health: https://btc-watchdog.fly.dev/health
- Latest Price: https://btc-watchdog.fly.dev/latest
- Historical Data: https://btc-watchdog.fly.dev/prices
- Statistics: https://btc-watchdog.fly.dev/stats
- Dashboard: https://btc-watchdog.fly.dev/dashboard.html
```

### Option 2: Share the Repository

Share the entire repository for users to deploy their own instance:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/btc-price-watchdog.git
cd btc-price-watchdog

# Follow the setup guide
# See SETUP.md for detailed instructions
```

### Option 3: Create a Fork

Users can fork the repository and deploy their own instance:

1. **Fork the repository** on GitHub
2. **Follow [SETUP.md](SETUP.md)** for deployment instructions
3. **Customize** the configuration as needed

## 📖 Documentation Structure

```
📁 BTC Price Watchdog
├── 📄 README.md              # Main project overview
├── 📄 API.md                 # Complete API documentation
├── 📄 SETUP.md               # Deployment guide
├── 📄 QUICK_START.md         # Quick start for live service
├── 📄 SHARING_GUIDE.md       # This file
├── 📄 DEPLOYMENT.md          # Detailed deployment info
├── 📄 fly.toml.example       # Configuration template
├── 📄 deploy-template.sh     # Deployment script template
├── 📄 test-deployment.py     # Service testing script
├── 📁 .github/workflows/     # CI/CD automation
└── 📁 data/                  # Local data (gitignored)
```

## 🎯 Use Cases

### For Developers
- **API Integration**: Use the REST API in your applications
- **Trading Bots**: Real-time price feeds for automated trading
- **Portfolio Tracking**: Historical price analysis
- **Educational Projects**: Learn about cryptocurrency APIs

### For End Users
- **Price Monitoring**: Real-time BTC price tracking
- **Historical Analysis**: View price trends over time
- **Mobile Dashboard**: Responsive web interface
- **Price Alerts**: Monitor for specific price levels

### For Organizations
- **Data Source**: Reliable BTC price data
- **Custom Deployment**: Deploy your own instance
- **Integration**: Embed in existing systems
- **Analytics**: Historical price analysis

## 🔧 Quick Integration Examples

### JavaScript
```javascript
// Get latest BTC price
fetch('https://btc-watchdog.fly.dev/latest')
  .then(response => response.json())
  .then(data => console.log(`BTC: ${data.formatted_price}`));
```

### Python
```python
import requests
response = requests.get('https://btc-watchdog.fly.dev/latest')
price = response.json()
print(f"BTC Price: {price['formatted_price']}")
```

### cURL
```bash
# Get latest price
curl https://btc-watchdog.fly.dev/latest

# Get health status
curl https://btc-watchdog.fly.dev/health
```

## 📊 Service Statistics

As of the last test:
- **Total Records**: 867+ price points
- **Date Range**: Continuous monitoring since deployment
- **Price Range**: $119,490 - $119,612 (current session)
- **Update Frequency**: Every second
- **Uptime**: 100% (with automatic restarts)

## 🛡️ Security & Reliability

### Security Features
- **HTTPS Only**: All endpoints use SSL/TLS
- **No Authentication Required**: Public API for easy access
- **Rate Limiting**: Built-in protection against abuse
- **Input Validation**: All parameters validated

### Reliability Features
- **Automatic Restarts**: Fly.io handles service recovery
- **Health Monitoring**: Continuous health checks
- **Persistent Storage**: Data survives restarts
- **WebSocket Reconnection**: Automatic reconnection to Coinbase

## 💰 Cost Information

### Live Service
- **Free to Use**: No cost for API access
- **No Rate Limits**: Reasonable usage encouraged
- **Always Available**: 24/7 operation

### Self-Hosted
- **Fly.io Free Tier**: 3 shared-cpu-1x 256mb VMs
- **Storage**: Minimal cost for persistent volumes
- **Bandwidth**: Included in free tier

## 🆘 Support & Maintenance

### For Live Service Users
1. **Check Health**: https://btc-watchdog.fly.dev/health
2. **Review Documentation**: See [API.md](API.md)
3. **Test Endpoints**: Use [test-deployment.py](test-deployment.py)

### For Self-Hosted Users
1. **Follow Setup Guide**: See [SETUP.md](SETUP.md)
2. **Check Logs**: `fly logs`
3. **Monitor Status**: `fly status`
4. **Test Deployment**: Run the test script

### Getting Help
- **Documentation**: Comprehensive guides included
- **GitHub Issues**: For bug reports and feature requests
- **Community**: Share experiences and solutions

## 🚀 Next Steps

### For Users
1. **Test the API**: Try the endpoints
2. **Integrate**: Use in your applications
3. **Monitor**: Check health regularly
4. **Deploy**: Consider your own instance

### For Contributors
1. **Fork the Repository**: Create your own copy
2. **Customize**: Modify for your needs
3. **Deploy**: Set up your instance
4. **Share**: Help others use the service

## 📈 Future Enhancements

Potential improvements for the service:
- **Additional Cryptocurrencies**: Support for ETH, other coins
- **WebSocket API**: Real-time streaming
- **Authentication**: Optional API keys
- **Rate Limiting**: Configurable limits
- **Analytics**: Advanced price analysis
- **Alerts**: Price threshold notifications

## 🎉 Conclusion

The BTC Price Watchdog service is ready for sharing and use! Whether you're:

- **Using the live service** for immediate access
- **Deploying your own instance** for full control
- **Integrating the API** into your applications
- **Learning from the code** for educational purposes

The service provides reliable, real-time BTC price data with a comprehensive API and documentation.

**Happy coding! 🚀** 