# BTC Price Watchdog - 24/7 Cloud Service

A 24/7 Bitcoin price monitoring service deployed on Fly.io with a persistent database and public API.

## Features

- 🔄 **Real-time BTC price monitoring** via Coinbase WebSocket
- 💾 **Persistent SQLite database** with Fly.io volumes
- 🌐 **Public REST API** for querying historical data
- 🏥 **Health monitoring** and automatic restarts
- 📊 **Statistics and analytics** endpoints
- 🐳 **Docker containerized** for easy deployment

## Quick Start

### Prerequisites

1. **Fly.io CLI**: Install with `curl -L https://fly.io/install.sh | sh`
2. **Fly.io Account**: Sign up at [fly.io](https://fly.io) and login with `fly auth login`

### Deployment

1. **Clone and navigate to the project**:
   ```bash
   cd coinbase-api/coinbase-btc
   ```

2. **Run the deployment script**:
   ```bash
   ./deploy.sh
   ```

   This script will:
   - Install Fly CLI if needed
   - Create the Fly.io app (`btc-watchdog`)
   - Create a persistent volume (`btc_data`)
   - Deploy the application
   - Show you the API endpoints

### Manual Deployment

If you prefer manual deployment:

```bash
# Create the app
fly apps create btc-watchdog --org personal

# Create persistent volume
fly volumes create btc_data --size 1 --region ord

# Deploy
fly deploy
```

## API Endpoints

Once deployed, your service will be available at `https://btc-watchdog.fly.dev`

### Base URL
```
https://btc-watchdog.fly.dev
```

### Endpoints

#### `GET /`
Service information and available endpoints.

#### `GET /health`
Health check endpoint.
```json
{
  "status": "healthy",
  "database": "healthy",
  "heartbeat": "active",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### `GET /latest`
Get the most recent BTC price.
```json
{
  "timestamp": "2024-01-01T12:00:00",
  "price": 45000.50,
  "formatted_price": "$45,000.50"
}
```

#### `GET /prices`
Query historical price data with optional filters.

**Parameters:**
- `start` (optional): Start timestamp (ISO format: "2024-01-01T00:00:00")
- `end` (optional): End timestamp (ISO format: "2024-01-02T00:00:00")
- `limit` (optional): Maximum records to return (1-1000, default: 100)

**Example:**
```bash
curl "https://btc-watchdog.fly.dev/prices?start=2024-01-01T00:00:00&end=2024-01-02T00:00:00&limit=50"
```

**Response:**
```json
{
  "count": 50,
  "prices": [
    {
      "timestamp": "2024-01-01T12:00:00",
      "price": 45000.50,
      "formatted_price": "$45,000.50"
    }
  ]
}
```

#### `GET /stats`
Get database statistics.
```json
{
  "total_records": 86400,
  "date_range": {
    "earliest": "2024-01-01T00:00:00",
    "latest": "2024-01-02T00:00:00"
  },
  "price_range": {
    "min": 44000.00,
    "max": 46000.00,
    "average": 45000.25
  },
  "database_path": "/data/btc_price_history.db"
}
```

## Monitoring and Management

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
fly ssh console -C "tail -f /data/btc_price_log.txt"
```

### Check Service Status
```bash
fly status
```

### Scale the Application
```bash
# Scale to 2 instances
fly scale count 2

# Change VM size
fly scale vm shared-cpu-2x
```

## Configuration

The service uses environment variables for configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_PATH` | `/data/btc_price_history.db` | SQLite database path |
| `LOG_PATH` | `/data/btc_price_log.txt` | Price log file path |
| `HEARTBEAT_PATH` | `/data/btc_logger_heartbeat.txt` | Heartbeat file path |
| `COINBASE_WS_URL` | `wss://ws-feed.exchange.coinbase.com` | Coinbase WebSocket URL |
| `TIMEZONE` | `America/New_York` | Timezone for timestamps |

## Local Development

### Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python app.py
```

### Test the API
```bash
# Health check
curl http://localhost:8000/health

# Latest price
curl http://localhost:8000/latest

# Price history
curl "http://localhost:8000/prices?limit=10"
```

## Database Schema

The service uses SQLite with a simple schema:

```sql
CREATE TABLE price_log (
    timestamp TEXT PRIMARY KEY,
    price REAL
);
```

- `timestamp`: ISO format timestamp (YYYY-MM-DDTHH:MM:SS)
- `price`: BTC price in USD

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Coinbase      │    │   Fly.io        │    │   Your App      │
│   WebSocket     │───▶│   Container     │───▶│   (Frontend)    │
│   Feed          │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Persistent    │
                       │   Volume        │
                       │   (/data)       │
                       └─────────────────┘
```

## Troubleshooting

### Service Not Starting
1. Check logs: `fly logs`
2. Verify health endpoint: `curl https://btc-watchdog.fly.dev/health`
3. Check volume mount: `fly ssh console -C "ls -la /data"`

### No Price Data
1. Check WebSocket connection: `fly logs | grep "WebSocket"`
2. Verify Coinbase API status
3. Check database: `fly ssh console -C "sqlite3 /data/btc_price_history.db 'SELECT COUNT(*) FROM price_log'"`

### High Memory Usage
1. Monitor with: `fly status`
2. Scale up: `fly scale vm shared-cpu-2x`
3. Check for memory leaks in logs

## Upgrading to PostgreSQL

For high-volume data (millions of records), consider upgrading to PostgreSQL:

```bash
# Create PostgreSQL database
fly postgres create --name btc-history-db --region ord

# Set database URL
fly secrets set DATABASE_URL="postgresql://..."

# Update code to use asyncpg instead of sqlite3
```

## License

MIT License - feel free to use this for your own projects! 