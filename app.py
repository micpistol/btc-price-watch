from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from btc_watchdog_service import log_btc_price

app = FastAPI(
    title="BTC Price Watchdog API",
    description="A 24/7 Bitcoin price monitoring service with historical data API",
    version="1.0.0"
)

# Mount static files for HTML dashboards
app.mount("/static", StaticFiles(directory="."), name="static")

# Configuration
DB_PATH = os.getenv("DB_PATH", "./data/btc_price_history.db")
LOG_PATH = os.getenv("LOG_PATH", "./data/btc_price_log.txt")
HEARTBEAT_PATH = os.getenv("HEARTBEAT_PATH", "./data/btc_logger_heartbeat.txt")

@app.on_event("startup")
async def startup_event():
    """Start the BTC price logger in the background on app startup"""
    print("🚀 Starting BTC Price Watchdog Service...")
    app.state.logger_task = asyncio.create_task(log_btc_price())
    print("✅ Background logger task started")

@app.on_event("shutdown")
async def shutdown_event():
    """Cancel the background logger task on app shutdown"""
    if hasattr(app.state, 'logger_task'):
        app.state.logger_task.cancel()
        try:
            await app.state.logger_task
        except asyncio.CancelledError:
            pass
    print("🛑 Background logger task stopped")

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if database exists and is accessible
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            conn.close()
            db_status = "healthy"
        else:
            db_status = "no_database"
        
        # Check heartbeat
        heartbeat_status = "unknown"
        if os.path.exists(HEARTBEAT_PATH):
            try:
                with open(HEARTBEAT_PATH, "r") as f:
                    heartbeat = f.read().strip()
                    heartbeat_status = "active" if heartbeat else "inactive"
            except:
                heartbeat_status = "error"
        
        return {
            "status": "healthy",
            "database": db_status,
            "heartbeat": heartbeat_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/latest")
async def get_latest_price():
    """Get the most recent BTC price"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, price FROM price_log 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''')
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "timestamp": result[0],
                "price": result[1],
                "formatted_price": f"${result[1]:,.2f}"
            }
        else:
            return {"message": "No price data available yet"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get latest price: {str(e)}")

@app.get("/prices")
async def get_prices(
    start: Optional[str] = None,
    end: Optional[str] = None,
    limit: Optional[int] = 100
):
    """
    Query historical BTC price data
    
    Args:
        start: Start timestamp (ISO format, e.g., "2024-01-01T00:00:00")
        end: End timestamp (ISO format, e.g., "2024-01-02T00:00:00")
        limit: Maximum number of records to return (default: 100, max: 1000)
    """
    try:
        # Validate limit
        if limit and (limit < 1 or limit > 1000):
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT timestamp, price FROM price_log"
        params = []
        
        conditions = []
        if start:
            conditions.append("timestamp >= ?")
            params.append(start)
        if end:
            conditions.append("timestamp <= ?")
            params.append(end)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        prices = [
            {
                "timestamp": row[0],
                "price": row[1],
                "formatted_price": f"${row[1]:,.2f}"
            }
            for row in results
        ]
        
        return {
            "count": len(prices),
            "prices": prices
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query prices: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get database statistics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM price_log")
        total_count = cursor.fetchone()[0]
        
        # Get date range
        cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM price_log")
        min_max = cursor.fetchone()
        date_range = {
            "earliest": min_max[0] if min_max[0] else None,
            "latest": min_max[1] if min_max[1] else None
        }
        
        # Get price range
        cursor.execute("SELECT MIN(price), MAX(price), AVG(price) FROM price_log")
        price_stats = cursor.fetchone()
        price_range = {
            "min": price_stats[0] if price_stats[0] else None,
            "max": price_stats[1] if price_stats[1] else None,
            "average": price_stats[2] if price_stats[2] else None
        }
        
        conn.close()
        
        return {
            "total_records": total_count,
            "date_range": date_range,
            "price_range": price_range,
            "database_path": DB_PATH
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.get("/price-changes")
async def get_price_changes():
    """Get 1h, 3h, 1d price changes from Kraken API"""
    try:
        import httpx
        
        # Fetch current price from our database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, price FROM price_log 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''')
        current_result = cursor.fetchone()
        conn.close()
        
        if not current_result:
            return {"message": "No price data available yet"}
        
        current_timestamp = current_result[0]
        current_price = current_result[1]
        
        # Fetch percentage changes directly from Kraken API
        async with httpx.AsyncClient() as client:
            # Kraken Ticker API for BTC/USD
            kraken_url = "https://api.kraken.com/0/public/Ticker"
            params = {"pair": "XBTUSD"}  # Kraken uses XBT for Bitcoin
            
            response = await client.get(kraken_url, params=params)
            if response.status_code == 200:
                data = response.json()
                
                if "result" in data and "XXBTZUSD" in data["result"]:
                    ticker = data["result"]["XXBTZUSD"]
                    
                    # Calculate percentage changes from Kraken data
                    changes = {}
                    
                    # 24 hour change (using opening price vs current price)
                    if "o" in ticker and "c" in ticker:
                        opening_price = float(ticker["o"])
                        current_kraken_price = float(ticker["c"][0])
                        day_change = ((current_kraken_price - opening_price) / opening_price) * 100
                        changes["1d"] = {
                            "percentage": round(day_change, 2),
                            "direction": "up" if day_change > 0 else "down" if day_change < 0 else "unchanged"
                        }
                    
                    # For 1h and 3h, we'll use our own database since Kraken doesn't provide these
                    # We can calculate from our historical data
                    from datetime import datetime, timedelta
                    from zoneinfo import ZoneInfo
                    
                    current_dt = datetime.fromisoformat(current_timestamp.replace('Z', '+00:00'))
                    
                    # 1 hour ago
                    one_hour_ago = current_dt - timedelta(hours=1)
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT price FROM price_log 
                        WHERE timestamp <= ? 
                        ORDER BY timestamp DESC 
                        LIMIT 1
                    ''', (one_hour_ago.strftime("%Y-%m-%dT%H:%M:%S"),))
                    one_hour_result = cursor.fetchone()
                    
                    if one_hour_result:
                        one_hour_price = one_hour_result[0]
                        one_hour_change = current_price - one_hour_price
                        one_hour_percent = (one_hour_change / one_hour_price) * 100
                        changes["1h"] = {
                            "percentage": round(one_hour_percent, 2),
                            "direction": "up" if one_hour_change > 0 else "down" if one_hour_change < 0 else "unchanged"
                        }
                    
                    # 3 hours ago
                    three_hours_ago = current_dt - timedelta(hours=3)
                    cursor.execute('''
                        SELECT price FROM price_log 
                        WHERE timestamp <= ? 
                        ORDER BY timestamp DESC 
                        LIMIT 1
                    ''', (three_hours_ago.strftime("%Y-%m-%dT%H:%M:%S"),))
                    three_hours_result = cursor.fetchone()
                    
                    if three_hours_result:
                        three_hours_price = three_hours_result[0]
                        three_hours_change = current_price - three_hours_price
                        three_hours_percent = (three_hours_change / three_hours_price) * 100
                        changes["3h"] = {
                            "percentage": round(three_hours_percent, 2),
                            "direction": "up" if three_hours_change > 0 else "down" if three_hours_change < 0 else "unchanged"
                        }
                    
                    conn.close()
                    
                    return {
                        "current_price": current_price,
                        "current_timestamp": current_timestamp,
                        "formatted_current_price": f"${current_price:,.2f}",
                        "changes": changes,
                        "source": "Kraken API"
                    }
        
        # Fallback if Kraken API fails
        return {
            "current_price": current_price,
            "current_timestamp": current_timestamp,
            "formatted_current_price": f"${current_price:,.2f}",
            "changes": {},
            "message": "Unable to fetch percentage changes from Kraken"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get price changes: {str(e)}")

@app.get("/dashboard")
async def get_dashboard():
    """Serve the desktop dashboard"""
    return FileResponse("dashboard.html")

@app.get("/mobile-dashboard")
async def get_mobile_dashboard():
    """Serve the mobile dashboard"""
    return FileResponse("mobile-dashboard.html")

@app.get("/frontend-example")
async def get_frontend_example():
    """Serve the frontend example"""
    return FileResponse("frontend_example.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 