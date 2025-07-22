#!/usr/bin/env python3
"""
BTC Price Watchdog Deployment Test Script

This script tests all endpoints of your BTC Price Watchdog service to ensure
it's working correctly after deployment.

Usage:
    python test-deployment.py [base_url]

Example:
    python test-deployment.py https://your-app-name.fly.dev
"""

import requests
import json
import sys
import time
from datetime import datetime, timedelta

def test_endpoint(url, endpoint, expected_status=200, description=""):
    """Test a single endpoint and return the result"""
    full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
    try:
        response = requests.get(full_url, timeout=10)
        success = response.status_code == expected_status
        print(f"{'✅' if success else '❌'} {description or endpoint}")
        print(f"   URL: {full_url}")
        print(f"   Status: {response.status_code}")
        
        if success and response.content:
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
            except:
                print(f"   Response: {response.text[:100]}...")
        
        print()
        return success, response
    except Exception as e:
        print(f"❌ {description or endpoint}")
        print(f"   URL: {full_url}")
        print(f"   Error: {str(e)}")
        print()
        return False, None

def test_health_endpoint(url):
    """Test the health endpoint and validate response structure"""
    success, response = test_endpoint(url, "/health", description="Health Check")
    
    if success and response:
        try:
            data = response.json()
            required_fields = ["status", "database", "heartbeat", "timestamp"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"   ⚠️  Missing fields: {missing_fields}")
                return False, response
            
            if data["status"] != "healthy":
                print(f"   ⚠️  Service status is not healthy: {data['status']}")
                return False, response
                
            print(f"   ✅ Service is healthy")
            print(f"   ✅ Database: {data['database']}")
            print(f"   ✅ Heartbeat: {data['heartbeat']}")
            return True, response
        except Exception as e:
            print(f"   ❌ Invalid JSON response: {str(e)}")
            return False, response
    
    return False, response

def test_latest_price(url):
    """Test the latest price endpoint"""
    success, response = test_endpoint(url, "/latest", description="Latest Price")
    
    if success and response:
        try:
            data = response.json()
            required_fields = ["timestamp", "price", "formatted_price"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"   ⚠️  Missing fields: {missing_fields}")
                return False, response
            
            # Validate price is a number
            if not isinstance(data["price"], (int, float)):
                print(f"   ⚠️  Price is not a number: {data['price']}")
                return False, response
            
            print(f"   ✅ Latest price: {data['formatted_price']}")
            print(f"   ✅ Timestamp: {data['timestamp']}")
            return True, response
        except Exception as e:
            print(f"   ❌ Invalid JSON response: {str(e)}")
            return False, response
    
    return False, response

def test_prices_endpoint(url):
    """Test the historical prices endpoint"""
    success, response = test_endpoint(url, "/prices", description="Historical Prices")
    
    if success and response:
        try:
            data = response.json()
            required_fields = ["prices", "count"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"   ⚠️  Missing fields: {missing_fields}")
                return False, response
            
            if not isinstance(data["prices"], list):
                print(f"   ⚠️  Prices is not a list: {type(data['prices'])}")
                return False, response
            
            print(f"   ✅ Retrieved {data['count']} price records")
            if data["prices"]:
                latest = data["prices"][0]
                print(f"   ✅ Latest record: {latest['timestamp']} - ${latest['price']}")
            
            return True, response
        except Exception as e:
            print(f"   ❌ Invalid JSON response: {str(e)}")
            return False, response
    
    return False, response

def test_stats_endpoint(url):
    """Test the statistics endpoint"""
    success, response = test_endpoint(url, "/stats", description="Service Statistics")
    
    if success and response:
        try:
            data = response.json()
            required_fields = ["total_records", "date_range", "price_range"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"   ⚠️  Missing fields: {missing_fields}")
                return False, response
            
            print(f"   ✅ Database records: {data.get('total_records', 'N/A')}")
            print(f"   ✅ Date range: {data['date_range'].get('earliest', 'N/A')} to {data['date_range'].get('latest', 'N/A')}")
            print(f"   ✅ Price range: ${data['price_range'].get('min', 'N/A')} - ${data['price_range'].get('max', 'N/A')}")
            return True, response
        except Exception as e:
            print(f"   ❌ Invalid JSON response: {str(e)}")
            return False, response
    
    return False, response

def test_with_parameters(url):
    """Test the prices endpoint with various parameters"""
    print("🔧 Testing with parameters...")
    
    # Test with limit parameter
    test_url = f"{url.rstrip('/')}/prices?limit=5"
    try:
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data["count"] <= 5:
                print(f"   ✅ Limit parameter works: {data['count']} records")
            else:
                print(f"   ⚠️  Limit parameter may not work: {data['count']} records")
        else:
            print(f"   ❌ Limit parameter test failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Limit parameter test error: {str(e)}")
    
    # Test with time range (last hour)
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    start_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")
    
    test_url = f"{url.rstrip('/')}/prices?start={start_str}&end={end_str}"
    try:
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Time range parameter works: {data['count']} records")
        else:
            print(f"   ❌ Time range parameter test failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Time range parameter test error: {str(e)}")
    
    print()

def main():
    """Main test function"""
    # Get base URL from command line or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "https://btc-watchdog.fly.dev"
    
    print("🚀 BTC Price Watchdog Deployment Test")
    print("=" * 50)
    print(f"Testing service at: {base_url}")
    print()
    
    # Test all endpoints
    tests = [
        ("Service Information", lambda: test_endpoint(base_url, "/", description="Service Information")),
        ("Health Check", lambda: test_health_endpoint(base_url)),
        ("Latest Price", lambda: test_latest_price(base_url)),
        ("Historical Prices", lambda: test_prices_endpoint(base_url)),
        ("Service Statistics", lambda: test_stats_endpoint(base_url)),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"📋 Testing: {test_name}")
        print("-" * 30)
        success, _ = test_func()
        if success:
            passed += 1
        print()
    
    # Test with parameters
    test_with_parameters(base_url)
    
    # Summary
    print("📊 Test Summary")
    print("=" * 50)
    print(f"Passed: {passed}/{total} tests")
    
    if passed == total:
        print("🎉 All tests passed! Your BTC Price Watchdog service is working correctly.")
        print()
        print("🌐 Your service is ready to use:")
        print(f"   - API Base URL: {base_url}")
        print(f"   - Health Check: {base_url}/health")
        print(f"   - Latest Price: {base_url}/latest")
        print(f"   - Historical Data: {base_url}/prices")
        print(f"   - Statistics: {base_url}/stats")
    else:
        print("⚠️  Some tests failed. Please check your deployment.")
        print("   - Verify the service is running: fly status")
        print("   - Check logs: fly logs")
        print("   - Ensure all environment variables are set correctly")

if __name__ == "__main__":
    main() 