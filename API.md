# BTC Price Watchdog API Documentation

Complete API reference for the BTC Price Watchdog service.

## Base URL

```
https://btc-watchdog.fly.dev
```

## Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

## Response Format

All API responses are returned in JSON format with the following structure:

### Success Response
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2024-01-01T12:00:00"
}
```

### Error Response
```json
{
  "detail": "Error message description"
}
```

## Endpoints

### 1. Service Information

#### `GET /`

Returns basic service information and available endpoints.

**Response:**
```json
{
  "service": "BTC Price Watchdog API",
  "status": "running",
  "version": "1.0.0",
  "endpoints": {
    "prices": "/prices - Query historical price data",
    "latest": "/latest - Get latest price",
    "health": "/health - Service health check",
    "stats": "/stats - Database statistics"
  }
}
```

**Example:**
```bash
curl https://btc-watchdog.fly.dev/
```

### 2. Health Check

#### `GET /health`

Returns the health status of the service and its components.

**Response:**
```json
{
  "status": "healthy",
  "database": "healthy",
  "heartbeat": "active",
  "timestamp": "2024-01-01T12:00:00"
}
```

**Status Values:**
- `database`: `healthy`, `no_database`, `error`
- `heartbeat`: `active`, `inactive`, `error`

**Example:**
```bash
curl https://btc-watchdog.fly.dev/health
```

### 3. Latest Price

#### `GET /latest`

Returns the most recent BTC price from the database.

**Response:**
```json
{
  "timestamp": "2024-01-01T12:00:00",
  "price": 45000.50,
  "formatted_price": "$45,000.50"
}
```

**Example:**
```bash
curl https://btc-watchdog.fly.dev/latest
```

### 4. Historical Prices

#### `GET /prices`

Returns historical BTC price data with optional filtering.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start` | string | No | null | Start timestamp (ISO format: YYYY-MM-DDTHH:MM:SS) |
| `end` | string | No | null | End timestamp (ISO format: YYYY-MM-DDTHH:MM:SS) |
| `limit` | integer | No | 100 | Maximum number of records to return (1-1000) |

**Response:**
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

**Examples:**

Get last 100 prices:
```bash
curl https://btc-watchdog.fly.dev/prices
```

Get last 50 prices:
```bash
curl https://btc-watchdog.fly.dev/prices?limit=50
```

Get prices from specific time range:
```bash
curl "https://btc-watchdog.fly.dev/prices?start=2024-01-01T00:00:00&end=2024-01-02T00:00:00"
```

Get prices from specific time with limit:
```bash
curl "https://btc-watchdog.fly.dev/prices?start=2024-01-01T00:00:00&limit=25"
```

### 5. Service Statistics

#### `GET /stats`

Returns statistics about the service and database.

**Response:**
```json
{
  "database_stats": {
    "total_records": 86400,
    "database_size_mb": 2.5,
    "oldest_record": "2024-01-01T00:00:00",
    "newest_record": "2024-01-01T23:59:00"
  },
  "service_stats": {
    "uptime_hours": 24,
    "last_heartbeat": "2024-01-01T23:59:00",
    "timezone": "America/New_York"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

**Example:**
```bash
curl https://btc-watchdog.fly.dev/stats
```

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Endpoint doesn't exist |
| 500 | Internal Server Error |

### Common Error Responses

**Invalid Date Format:**
```json
{
  "detail": "Invalid date format. Use ISO format: YYYY-MM-DDTHH:MM:SS"
}
```

**Invalid Limit Parameter:**
```json
{
  "detail": "Limit must be between 1 and 1000"
}
```

**Database Error:**
```json
{
  "detail": "Database error: unable to connect"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. However, please be respectful and avoid excessive requests.

## Data Format

### Timestamps

All timestamps are in ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`

### Prices

Prices are returned as floating-point numbers representing USD values.

### Timezone

All timestamps are in the timezone specified by the `TIMEZONE` environment variable (default: America/New_York).

## Data Retention

- Price data is stored in a SQLite database
- Data is stored on Fly.io persistent volumes
- No automatic data cleanup is implemented
- Historical data is available as long as the service is running

## WebSocket Data Source

The service receives real-time BTC price data from Coinbase WebSocket feed:
- Product: BTC-USD
- Update frequency: Every second
- Data source: `wss://ws-feed.exchange.coinbase.com`

## Integration Examples

### JavaScript/Node.js

```javascript
// Get latest price
async function getLatestPrice() {
  const response = await fetch('https://btc-watchdog.fly.dev/latest');
  const data = await response.json();
  return data;
}

// Get historical prices
async function getHistoricalPrices(start, end, limit = 100) {
  const params = new URLSearchParams();
  if (start) params.append('start', start);
  if (end) params.append('end', end);
  if (limit) params.append('limit', limit.toString());
  
  const response = await fetch(`https://btc-watchdog.fly.dev/prices?${params}`);
  const data = await response.json();
  return data;
}

// Monitor price changes
async function monitorPrice() {
  const checkPrice = async () => {
    const price = await getLatestPrice();
    console.log(`BTC: ${price.formatted_price} at ${price.timestamp}`);
  };
  
  // Check every 5 seconds
  setInterval(checkPrice, 5000);
  checkPrice(); // Initial check
}
```

### Python

```python
import requests
import json

def get_latest_price():
    response = requests.get('https://btc-watchdog.fly.dev/latest')
    return response.json()

def get_historical_prices(start=None, end=None, limit=100):
    params = {}
    if start:
        params['start'] = start
    if end:
        params['end'] = end
    if limit:
        params['limit'] = limit
    
    response = requests.get('https://btc-watchdog.fly.dev/prices', params=params)
    return response.json()

def check_service_health():
    response = requests.get('https://btc-watchdog.fly.dev/health')
    return response.json()

# Example usage
if __name__ == "__main__":
    # Get latest price
    latest = get_latest_price()
    print(f"Latest BTC price: {latest['formatted_price']}")
    
    # Get last 10 prices
    history = get_historical_prices(limit=10)
    print(f"Retrieved {history['count']} price records")
```

### cURL Examples

```bash
# Get latest price
curl -s https://btc-watchdog.fly.dev/latest | jq '.'

# Get prices from last hour
curl -s "https://btc-watchdog.fly.dev/prices?limit=3600" | jq '.prices | length'

# Check service health
curl -s https://btc-watchdog.fly.dev/health | jq '.'

# Get service statistics
curl -s https://btc-watchdog.fly.dev/stats | jq '.'
```

## Support

For issues or questions:
1. Check the health endpoint first
2. Review the service logs (if you have access)
3. Consider deploying your own instance for full control
4. Check the [README.md](README.md) for additional documentation

## Changelog

### Version 1.0.0
- Initial release
- Real-time BTC price monitoring
- Historical data API
- Health monitoring
- Statistics endpoint 