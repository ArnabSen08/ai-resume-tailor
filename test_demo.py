#!/usr/bin/env python3
"""
Test the demo version of AI Resume Tailor
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_demo():
    print("🧪 Testing AI Resume Tailor Demo")
    print("=" * 40)
    
    # Test health
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Health Check: {response.json()}")
    
    # Test resume tailoring
    sample_resume = """
John Doe
Software Engineer

Experience:
- Developed web applications using Python
- Worked with databases and APIs
- Collaborated with teams

Skills: Python, JavaScript, SQL
"""
    
    sample_job = """
We are looking for a Senior Python Developer with:
- FastAPI experience
- React frontend skills
- AWS cloud knowledge
- Machine learning background
"""
    
    payload = {
        "resume": sample_resume,
        "job_desc": sample_job
    }
    
    print("\n🔄 Testing resume optimization...")
    response = requests.post(f"{BASE_URL}/tailor-resume", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Resume optimization successful!")
        print(f"📝 Optimized resume preview: {result['tailored_resume'][:100]}...")
        print(f"🎯 Skills extracted: {result['key_skills_extracted']}")
        print(f"📋 Notes: {result['optimization_notes']}")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_demo()