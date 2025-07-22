# BTC Price Watchdog - Documentation Index

Welcome to the BTC Price Watchdog documentation! This index will help you find the information you need.

## 📚 Documentation Files

### 🚀 Getting Started
- **[README.md](README.md)** - Main project overview and introduction
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide for using the live service
- **[SHARING_GUIDE.md](SHARING_GUIDE.md)** - How to share and use the service

### 🔧 Setup & Deployment
- **[SETUP.md](SETUP.md)** - Complete setup guide for deploying your own instance
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Detailed deployment information
- **[fly.toml.example](fly.toml.example)** - Configuration template
- **[deploy-template.sh](deploy-template.sh)** - Deployment script template

### 📖 API Reference
- **[API.md](API.md)** - Complete API documentation with examples
- **[test-deployment.py](test-deployment.py)** - Service testing script

### 🎯 Use Cases & Examples
- **[dashboard.html](dashboard.html)** - Desktop dashboard example
- **[mobile-dashboard.html](mobile-dashboard.html)** - Mobile dashboard example
- **[frontend_example.html](frontend_example.html)** - Frontend integration example

## 🎯 Quick Navigation

### I want to...
- **Use the live service** → [QUICK_START.md](QUICK_START.md)
- **Deploy my own instance** → [SETUP.md](SETUP.md)
- **Learn about the API** → [API.md](API.md)
- **Share the service** → [SHARING_GUIDE.md](SHARING_GUIDE.md)
- **Test the service** → [test-deployment.py](test-deployment.py)
- **Understand the project** → [README.md](README.md)

## 🌐 Live Service

The BTC Price Watchdog service is currently running at:
**https://btc-watchdog.fly.dev**

### Quick Test
```bash
# Check if the service is working
curl https://btc-watchdog.fly.dev/health

# Get the latest BTC price
curl https://btc-watchdog.fly.dev/latest
```

## 📋 Service Status

✅ **Service is healthy and operational**
- Real-time BTC price monitoring
- 5 API endpoints available
- Persistent data storage
- Automatic health monitoring

## 🔗 External Resources

- **Fly.io Documentation**: https://fly.io/docs/
- **Coinbase API**: https://docs.cloud.coinbase.com/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/

## 📞 Support

If you need help:
1. Check the relevant documentation above
2. Test the service using the test script
3. Review the API documentation
4. Consider deploying your own instance for full control

---

**Happy coding! 🚀** 