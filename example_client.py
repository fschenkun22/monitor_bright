#!/usr/bin/env python3
"""
Example client script for Monitor Brightness API
Demonstrates how to interact with the API endpoints
"""
import requests
import json
import sys


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))


def main():
    base_url = "http://localhost:5000"
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"Testing Monitor Brightness API at {base_url}")
    
    # 1. Get API documentation
    try:
        response = requests.get(f"{base_url}/")
        print_response("API Documentation", response)
    except Exception as e:
        print(f"Error connecting to API: {e}")
        sys.exit(1)
    
    # 2. Health check
    response = requests.get(f"{base_url}/api/health")
    print_response("Health Check", response)
    
    # 3. List monitors
    response = requests.get(f"{base_url}/api/monitors")
    print_response("List Monitors", response)
    
    # 4. Get current brightness
    response = requests.get(f"{base_url}/api/brightness")
    print_response("Get Current Brightness", response)
    
    # 5. Set brightness to 80%
    response = requests.post(
        f"{base_url}/api/brightness",
        json={"brightness": 80}
    )
    print_response("Set Brightness to 80%", response)
    
    # 6. Test validation - invalid brightness (too high)
    response = requests.post(
        f"{base_url}/api/brightness",
        json={"brightness": 150}
    )
    print_response("Test Validation - Invalid Value (150)", response)
    
    # 7. Test validation - missing parameter
    response = requests.post(
        f"{base_url}/api/brightness",
        json={}
    )
    print_response("Test Validation - Missing Parameter", response)
    
    print(f"\n{'='*60}")
    print("Testing complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
