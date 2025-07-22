# BTC Price Watchdog - Quick Start Guide

Want to use the BTC Price Watchdog service right now? Here's how to get started in minutes!

## 🌐 Live Service

The BTC Price Watchdog service is currently running at:
**https://btc-watchdog.fly.dev**

## 🚀 Quick API Examples

### 1. Check Service Health
```bash
curl https://btc-watchdog.fly.dev/health
```

### 2. Get Latest BTC Price
```bash
curl https://btc-watchdog.fly.dev/latest
```

### 3. Get Historical Prices
```bash
# Last 100 prices
curl https://btc-watchdog.fly.dev/prices

# Last 50 prices
curl https://btc-watchdog.fly.dev/prices?limit=50

# Prices from specific time range
curl "https://btc-watchdog.fly.dev/prices?start=2024-01-01T00:00:00&end=2024-01-02T00:00:00"
```

### 4. Get Service Statistics
```bash
curl https://btc-watchdog.fly.dev/stats
```

## 📊 Web Dashboard

Visit the live dashboard to see real-time BTC price data:
- **Desktop Dashboard**: https://btc-watchdog.fly.dev/dashboard.html
- **Mobile Dashboard**: https://btc-watchdog.fly.dev/mobile-dashboard.html

## 🔧 JavaScript Integration

### Fetch Latest Price
```javascript
fetch('https://btc-watchdog.fly.dev/latest')
  .then(response => response.json())
  .then(data => {
    console.log(`BTC Price: ${data.formatted_price}`);
    console.log(`Timestamp: ${data.timestamp}`);
  });
```

### Fetch Historical Data
```javascript
fetch('https://btc-watchdog.fly.dev/prices?limit=100')
  .then(response => response.json())
  .then(data => {
    data.prices.forEach(price => {
      console.log(`${price.timestamp}: $${price.price}`);
    });
  });
```

## 📱 Mobile App Integration

### iOS Swift Example
```swift
let url = URL(string: "https://btc-watchdog.fly.dev/latest")!
URLSession.shared.dataTask(with: url) { data, response, error in
    if let data = data {
        let priceData = try? JSONDecoder().decode(PriceData.self, from: data)
        print("BTC Price: \(priceData?.formatted_price ?? "N/A")")
    }
}.resume()
```

### Android Kotlin Example
```kotlin
val url = URL("https://btc-watchdog.fly.dev/latest")
val connection = url.openConnection() as HttpURLConnection
val inputStream = connection.inputStream
val response = inputStream.bufferedReader().use { it.readText() }
// Parse JSON response
```

## 📈 Data Format

### Latest Price Response
```json
{
  "timestamp": "2024-01-01T12:00:00",
  "price": 45000.50,
  "formatted_price": "$45,000.50"
}
```

### Historical Prices Response
```json
{
  "prices": [
    {
      "timestamp": "2024-01-01T12:00:00",
      "price": 45000.50
    },
    {
      "timestamp": "2024-01-01T11:59:00",
      "price": 44995.25
    }
  ],
  "count": 2,
  "query": {
    "start": null,
    "end": null,
    "limit": 100
  }
}
```

## 🔄 Real-time Updates

The service updates BTC prices every second via Coinbase WebSocket feed. Historical data is stored in a persistent database.

## 📊 Service Statistics

Get insights about the service:
```bash
curl https://btc-watchdog.fly.dev/stats
```

Response includes:
- Total price records
- Database size
- Service uptime
- Latest price timestamp

## 🛠️ Error Handling

The API returns standard HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid parameters)
- `500`: Server error

Example error response:
```json
{
  "detail": "Invalid date format. Use ISO format: YYYY-MM-DDTHH:MM:SS"
}
```

## 🔗 API Documentation

For complete API documentation, see:
- [README.md](README.md) - Full API reference
- [SETUP.md](SETUP.md) - Deploy your own instance

## 🆘 Support

If you encounter issues:
1. Check the health endpoint: `https://btc-watchdog.fly.dev/health`
2. Review the service logs (if you have access)
3. Consider deploying your own instance for full control

## 🎯 Use Cases

- **Trading bots**: Real-time price feeds
- **Portfolio tracking**: Historical price analysis
- **Price alerts**: Monitor for specific price levels
- **Data analysis**: Historical BTC price trends
- **Educational projects**: Learn about cryptocurrency APIs

## 🚀 Next Steps

1. **Test the API endpoints** to ensure they meet your needs
2. **Integrate into your application** using the examples above
3. **Deploy your own instance** for full control (see [SETUP.md](SETUP.md))
4. **Customize the service** to add your own features

Happy coding! 🚀 