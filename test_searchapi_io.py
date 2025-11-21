#!/usr/bin/env python3
"""Test SearchAPI.io to see actual response structure"""
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
api_key = os.getenv("SEARCHAPI_KEY", "").strip()

if not api_key:
    print("❌ SEARCHAPI_KEY not found")
    exit(1)

print("Testing SearchAPI.io...")
print(f"Key: {api_key[:10]}...{api_key[-10:]}")
print()

url = "https://www.searchapi.io/api/v1/search"
params = {
    "engine": "google_shopping",
    "q": "iPhone",
    "api_key": api_key,
    "gl": "sa",
    "hl": "ar",
    "google_domain": "google.com.sa",
    "location": "Riyadh, Saudi Arabia",
}

try:
    r = requests.get(url, params=params, timeout=30)
    print(f"Status: {r.status_code}")
    print()
    
    if r.status_code == 200:
        data = r.json()
        print("✅ SUCCESS!")
        print()
        print("Response keys:", list(data.keys())[:10])
        print()
        
        # Check for shopping results
        if "shopping_results" in data:
            results = data["shopping_results"]
            print(f"Found {len(results)} shopping results")
            if results:
                print("\nFirst result:")
                print(json.dumps(results[0], indent=2, ensure_ascii=False))
        else:
            print("⚠️  No 'shopping_results' key found")
            print("\nFull response structure:")
            print(json.dumps({k: type(v).__name__ for k, v in list(data.items())[:20]}, indent=2))
            
    elif r.status_code == 401:
        print("❌ 401 Unauthorized")
        try:
            error = r.json()
            print(f"Error: {error}")
        except:
            print(f"Response: {r.text[:500]}")
    else:
        print(f"❌ Error {r.status_code}")
        print(r.text[:500])
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()

