#!/usr/bin/env python3
"""
Test script for the BTC Price Watchdog API
Run this to verify all endpoints are working correctly
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"  # Change to your Fly.io URL when deployed

def test_endpoint(endpoint, description):
    """Test an API endpoint and print results"""
    print(f"\n🔍 Testing {description}...")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_prices_with_params():
    """Test the prices endpoint with various parameters"""
    print(f"\n🔍 Testing prices endpoint with parameters...")
    
    # Test with limit
    try:
        response = requests.get(f"{BASE_URL}/prices?limit=5", timeout=10)
        print(f"✅ Prices with limit=5: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Found {data.get('count', 0)} prices")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test with date range (last 24 hours)
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        start_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        end_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        response = requests.get(f"{BASE_URL}/prices?start={start_str}&end={end_str}&limit=10", timeout=10)
        print(f"✅ Prices with date range: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Found {data.get('count', 0)} prices in date range")
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Run all API tests"""
    print("🚀 Starting BTC Price Watchdog API Tests")
    print(f"📍 Testing against: {BASE_URL}")
    
    # Test basic endpoints
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/latest", "Latest price"),
        ("/stats", "Statistics"),
    ]
    
    results = []
    for endpoint, description in endpoints:
        success = test_endpoint(endpoint, description)
        results.append((description, success))
    
    # Test prices endpoint with parameters
    test_prices_with_params()
    
    # Summary
    print(f"\n📊 Test Summary:")
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {description}")
    
    print(f"\n🎉 Testing complete!")
    print(f"💡 If running locally, make sure the service is started with: python app.py")
    print(f"🌐 If testing deployed service, update BASE_URL in this script")

if __name__ == "__main__":
    main() 