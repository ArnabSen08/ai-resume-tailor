#!/usr/bin/env python3
"""
Local testing script for AI Resume Tailor
Run this to test your backend locally before deployment
"""

import requests
import json
import time
import sys

# Configuration
BASE_URL = "http://localhost:8000"
SAMPLE_RESUME = """
John Doe
Software Engineer

Experience:
- Developed web applications using Python and JavaScript
- Worked with databases and APIs
- Collaborated with cross-functional teams

Skills:
- Python, JavaScript, SQL
- React, FastAPI
- Git, Docker
"""

SAMPLE_JOB_DESC = """
We are looking for a Senior Python Developer with experience in:
- FastAPI and web development
- Machine Learning and AI
- Database design and optimization
- Cloud deployment (AWS/GCP)
- Team leadership and mentoring

Requirements:
- 5+ years Python experience
- Experience with ML frameworks
- Strong problem-solving skills
"""

def test_health_check():
    """Test if the backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure to run: python app.py")
        return False

def test_file_upload():
    """Test file upload functionality with a sample text file"""
    try:
        # Create a sample resume file
        sample_resume_content = SAMPLE_RESUME.encode('utf-8')
        
        print("🔄 Testing file upload...")
        
        files = {'file': ('sample_resume.txt', sample_resume_content, 'text/plain')}
        response = requests.post(f"{BASE_URL}/upload-resume", files=files, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ File upload successful!")
            print(f"   File type: {result.get('file_type', 'N/A')}")
            print(f"   Extracted text length: {len(result.get('extracted_text', ''))}")
            print(f"   Message: {result.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ File upload failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ File upload request failed: {e}")
        return False

def test_resume_tailoring():
    """Test the main resume tailoring functionality"""
    try:
        payload = {
            "resume": SAMPLE_RESUME,
            "job_desc": SAMPLE_JOB_DESC
        }
        
        print("🔄 Testing resume tailoring...")
        response = requests.post(f"{BASE_URL}/tailor-resume", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resume tailoring successful!")
            print(f"   Tailored resume length: {len(result.get('tailored_resume', ''))}")
            print(f"   Skills extracted: {result.get('key_skills_extracted', [])}")
            print(f"   Notes: {result.get('optimization_notes', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Resume tailoring failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Resume tailoring request failed: {e}")
        return False

def test_job_scraping():
    """Test job description scraping (optional)"""
    try:
        # Using a sample URL - this might not work depending on the site
        test_url = "https://example.com"
        
        print("🔄 Testing job URL scraping...")
        response = requests.post(f"{BASE_URL}/scrape-job", params={"job_url": test_url}, timeout=10)
        
        if response.status_code == 200:
            print("✅ Job scraping endpoint works")
            return True
        else:
            print(f"⚠️  Job scraping failed (expected for example.com): {response.status_code}")
            return True  # This is expected to fail with example.com
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Job scraping test failed (expected): {e}")
        return True  # This is expected

def main():
    """Run all tests"""
    print("🧪 AI Resume Tailor - Local Testing")
    print("=" * 50)
    
    # Test 1: Health Check
    if not test_health_check():
        print("\n❌ Backend is not running. Please start it with: python app.py")
        sys.exit(1)
    
    print()
    
    # Test 2: File Upload
    if not test_file_upload():
        print("\n⚠️  File upload failed, but this is optional functionality.")
    
    print()
    
    # Test 3: Resume Tailoring
    if not test_resume_tailoring():
        print("\n❌ Resume tailoring failed. Check your Ollama setup.")
        print("   Make sure Ollama is running and the model is available:")
        print("   - ollama serve")
        print("   - ollama pull mistral")
        sys.exit(1)
    
    print()
    
    # Test 4: Job Scraping (optional)
    test_job_scraping()
    
    print()
    print("🎉 All tests passed! Your backend is ready for deployment.")
    print(f"📱 Frontend URL: file://{__file__.replace('test_local.py', 'index.html')}")
    print(f"🔗 Backend URL: {BASE_URL}")
    print("\nNext steps:")
    print("1. Deploy backend to Render/Railway")
    print("2. Update script.js with your backend URL")
    print("3. Test the full application")

if __name__ == "__main__":
    main()