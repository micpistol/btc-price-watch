FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /data

# Set environment variables
ENV DB_PATH=/data/btc_price_history.db
ENV LOG_PATH=/data/btc_price_log.txt
ENV HEARTBEAT_PATH=/data/btc_logger_heartbeat.txt
ENV COINBASE_WS_URL=wss://ws-feed.exchange.coinbase.com
ENV TIMEZONE=America/New_York

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 