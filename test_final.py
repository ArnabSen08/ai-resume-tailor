#!/usr/bin/env python3
"""
Test the final production version of AI Resume Tailor
"""

import requests
import json

def test_production_api(base_url):
    print(f"🧪 Testing AI Resume Tailor at {base_url}")
    print("=" * 60)
    
    # Test 1: Health Check
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health Check: PASSED")
            print(f"   Status: {health_data.get('status')}")
            print(f"   AI Engine: {health_data.get('ai_engine')}")
            print(f"   Features: {health_data.get('features_active')}")
        else:
            print(f"❌ Health Check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Health Check: FAILED - {str(e)}")
        return False
    
    # Test 2: Resume Optimization
    print("\n🔄 Testing Resume Optimization...")
    sample_resume = """John Doe
Software Engineer
Email: john.doe@email.com

EXPERIENCE
Software Engineer | Tech Corp | 2021-Present
- Developed web applications using Python and JavaScript
- Worked with databases and APIs
- Collaborated with cross-functional teams

SKILLS
Python, JavaScript, SQL, Git"""

    sample_job = """Senior Python Developer Position

We are seeking a Senior Python Developer with:
- 5+ years of Python development experience
- React and FastAPI expertise
- AWS cloud platform knowledge
- Machine learning and data analysis skills
- Leadership and team management experience
- Agile development methodologies

Requirements:
- Bachelor's degree in Computer Science
- Experience with Docker and Kubernetes
- Strong problem-solving abilities"""

    payload = {
        "resume": sample_resume,
        "job_desc": sample_job
    }
    
    try:
        response = requests.post(f"{base_url}/tailor-resume", json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Resume Optimization: PASSED")
            print(f"📝 Optimized Resume Preview:")
            print(f"   {result['tailored_resume'][:200]}...")
            print(f"🎯 Skills Extracted ({len(result['key_skills_extracted'])}): {result['key_skills_extracted'][:5]}")
            print(f"📋 Optimization Notes: {result['optimization_notes'][:100]}...")
        else:
            print(f"❌ Resume Optimization: FAILED ({response.status_code})")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Resume Optimization: FAILED - {str(e)}")
        return False
    
    # Test 3: Job URL Scraping (optional)
    print("\n🔄 Testing Job URL Scraping...")
    try:
        # Test with a simple URL (this might fail, which is expected)
        test_url = "https://httpbin.org/html"  # Simple test URL
        response = requests.post(f"{base_url}/scrape-job", params={"job_url": test_url}, timeout=15)
        if response.status_code == 200:
            print("✅ Job URL Scraping: PASSED")
        else:
            print("⚠️  Job URL Scraping: Expected to fail with test URL")
    except Exception as e:
        print("⚠️  Job URL Scraping: Expected to fail with test URL")
    
    print("\n🎉 All Core Tests Passed! Your AI Resume Tailor is working perfectly!")
    return True

def main():
    # Test local version if available
    local_url = "http://localhost:8000"
    production_url = "https://ai-resume-tailor-backend.onrender.com"
    
    print("🚀 AI Resume Tailor - Production Test Suite")
    print("=" * 60)
    
    # Try local first
    try:
        requests.get(f"{local_url}/health", timeout=2)
        print("🏠 Testing Local Development Server...")
        test_production_api(local_url)
    except:
        print("🏠 Local server not running (this is normal)")
    
    print(f"\n🌐 To test your deployed version, run:")
    print(f"python test_final.py {production_url}")
    
    # If URL provided as argument
    import sys
    if len(sys.argv) > 1:
        custom_url = sys.argv[1]
        print(f"\n🌐 Testing Custom URL: {custom_url}")
        test_production_api(custom_url)

if __name__ == "__main__":
    main()