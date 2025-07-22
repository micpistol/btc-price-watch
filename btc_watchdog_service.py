import asyncio
import websockets
import json
from datetime import datetime
from datetime import timezone
from zoneinfo import ZoneInfo
import sqlite3
import os
import sys

# Configuration from environment variables
DB_PATH = os.getenv("DB_PATH", "./data/btc_price_history.db")
LOG_PATH = os.getenv("LOG_PATH", "./data/btc_price_log.txt")
HEARTBEAT_PATH = os.getenv("HEARTBEAT_PATH", "./data/btc_logger_heartbeat.txt")
COINBASE_WS_URL = os.getenv("COINBASE_WS_URL", "wss://ws-feed.exchange.coinbase.com")
TIMEZONE = os.getenv("TIMEZONE", "America/New_York")

last_logged_second = None

def ensure_data_dirs():
    """Ensure all data directories exist"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(HEARTBEAT_PATH), exist_ok=True)

def init_database():
    """Initialize the SQLite database with the price_log table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_log (
            timestamp TEXT PRIMARY KEY,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_tick(timestamp: str, price: float):
    """Insert a price tick into the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    dt = datetime.now(ZoneInfo(TIMEZONE)).replace(microsecond=0)
    rounded_timestamp = dt.strftime("%Y-%m-%dT%H:%M:%S")
    cursor.execute('''
        INSERT OR REPLACE INTO price_log (timestamp, price) VALUES (?, ?)
    ''', (rounded_timestamp, price))
    conn.commit()
    conn.close()

async def log_btc_price():
    """Main coroutine for logging BTC prices from Coinbase WebSocket"""
    global last_logged_second
    
    # Ensure directories exist
    ensure_data_dirs()
    init_database()

    while True:
        try:
            async with websockets.connect(COINBASE_WS_URL) as websocket:
                subscribe_message = {
                    "type": "subscribe",
                    "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
                }
                await websocket.send(json.dumps(subscribe_message))
                print(f"✅ Connected to Coinbase WebSocket and subscribed to BTC-USD")

                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=10)
                        data = json.loads(message)

                        if data.get("type") != "ticker" or "price" not in data:
                            continue

                        price = float(data["price"])
                        now = datetime.now(ZoneInfo(TIMEZONE))
                        now = now.replace(microsecond=0)

                        current_second = int(now.timestamp())
                        if last_logged_second == current_second:
                            continue
                        last_logged_second = current_second

                        rounded_timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")
                        formatted_price = f"${price:,.2f}"
                        log_entry = f"{rounded_timestamp} | {formatted_price}\n"

                        # Write to log file
                        with open(LOG_PATH, "a") as f:
                            f.write(log_entry)

                        # Insert into database
                        insert_tick(rounded_timestamp, price)

                        # Update heartbeat
                        with open(HEARTBEAT_PATH, "w") as hb:
                            hb.write(f"{rounded_timestamp} BTC logger alive\n")

                        print(f"📊 Logged BTC price: {formatted_price} at {rounded_timestamp}")

                    except asyncio.TimeoutError:
                        print("⚠️ WebSocket timeout. Reconnecting...")
                        break
        except Exception as e:
            print("⚠️ Logger encountered an error:", e)
            import traceback
            traceback.print_exc()
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(log_btc_price()) 