#!/usr/bin/env python3
"""
Quick script to export participant data from Architector Analytics Backend
"""

import requests
import json
from datetime import datetime

BACKEND_URL = "https://architector-analytics.onrender.com"

print("🔍 Fetching participant data from Render backend...")
print(f"URL: {BACKEND_URL}/architector/stats\n")

try:
    response = requests.get(f"{BACKEND_URL}/architector/stats", timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        
        print("=" * 70)
        print("📊 PARTICIPANT DATA SUMMARY")
        print("=" * 70)
        
        # Overall stats
        print(f"\n✅ Total Participants: {data.get('total_participants', 0)}")
        print(f"✅ Total Sessions: {data.get('total_sessions', 0)}")
        print(f"✅ Success Rate: {data.get('success_rate', 0) * 100:.1f}%")
        
        # Participant details
        if 'participants' in data:
            print(f"\n{'=' * 70}")
            print("👥 PARTICIPANT DETAILS")
            print("=" * 70)
            
            for i, participant in enumerate(data['participants'], 1):
                print(f"\n[Participant {i}]")
                print(f"  ID: {participant.get('participant_id', 'N/A')}")
                print(f"  Name: {participant.get('full_name', 'N/A')}")
                print(f"  Email: {participant.get('email', 'N/A')}")
                print(f"  Designation: {participant.get('designation', 'N/A')}")
                print(f"  Experience: {participant.get('experience_level', 'N/A')}")
                print(f"  Organization: {participant.get('organization', 'N/A')}")
                print(f"  Country: {participant.get('country', 'N/A')}")
                print(f"  Registered: {participant.get('consent_timestamp', 'N/A')}")
                print(f"  Extension Version: {participant.get('extension_version', 'N/A')}")
        
        # Session summary
        if 'sessions' in data:
            print(f"\n{'=' * 70}")
            print("📈 SESSION SUMMARY")
            print("=" * 70)
            print(f"\nTotal Sessions: {len(data['sessions'])}")
            
            if data['sessions']:
                languages = {}
                for session in data['sessions']:
                    lang = session.get('project_language', 'Unknown')
                    languages[lang] = languages.get(lang, 0) + 1
                
                print("\nLanguage Distribution:")
                for lang, count in sorted(languages.items()):
                    print(f"  {lang}: {count} session(s)")
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"participant_data_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n{'=' * 70}")
        print(f"✅ Data saved to: {filename}")
        print(f"{'=' * 70}")
        
    else:
        print(f"❌ Error: Received status code {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.Timeout:
    print("⏰ Request timed out. Backend might be sleeping (Render free tier).")
    print("💡 Try again in 30 seconds (Render is waking up).")
    
except requests.exceptions.RequestException as e:
    print(f"❌ Network error: {e}")
    print("\n💡 Troubleshooting:")
    print("   1. Check if backend is running on Render")
    print("   2. Verify URL: https://architector-analytics.onrender.com")
    print("   3. Check Render logs for errors")

except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\n📚 For detailed instructions, see: PARTICIPANT_DATA_GUIDE.md")
