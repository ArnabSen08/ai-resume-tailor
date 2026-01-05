from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from typing import Optional, List
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Resume Tailor", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeRequest(BaseModel):
    resume: str
    job_desc: str
    job_url: Optional[str] = None

class ResumeResponse(BaseModel):
    tailored_resume: str
    key_skills_extracted: List[str]
    optimization_notes: str

# Configuration - Use environment variables for production
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "mistral")
USE_DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

def extract_job_description_from_url(url: str) -> str:
    """
    Extract job description from URL using web scraping
    """
    try:
        from bs4 import BeautifulSoup
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Common job description selectors for popular job sites
        job_desc_selectors = [
            '.job-description',
            '.jobsearch-jobDescriptionText',
            '[data-testid="job-description"]',
            '.job-details',
            '.description',
            '.job-content',
            '.posting-description'
        ]
        
        job_description = ""
        for selector in job_desc_selectors:
            element = soup.select_one(selector)
            if element:
                job_description = element.get_text(strip=True)
                break
        
        if not job_description:
            # Fallback: get all paragraph text
            paragraphs = soup.find_all('p')
            job_description = ' '.join([p.get_text(strip=True) for p in paragraphs])
        
        return job_description[:5000]  # Limit to 5000 chars
        
    except Exception as e:
        logger.error(f"Error scraping job URL: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Could not scrape job URL: {str(e)}")

def call_ollama_api(prompt: str) -> str:
    """
    Call Ollama API with the given prompt
    """
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2000
            }
        }
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Ollama API error: {response.text}")
        
        result = response.json()
        return result.get("response", "")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama API request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to connect to Ollama: {str(e)}")

def mock_ai_optimization(resume: str, job_desc: str) -> dict:
    """
    Mock AI optimization for demo purposes
    """
    # Extract some keywords from job description
    job_words = job_desc.lower().split()
    skills = []
    
    # Common tech skills to look for
    tech_skills = ['python', 'javascript', 'react', 'fastapi', 'sql', 'aws', 'docker', 'kubernetes', 'machine learning', 'ai', 'data', 'analytics', 'node.js', 'typescript', 'mongodb', 'postgresql', 'git', 'agile', 'scrum']
    
    for skill in tech_skills:
        if skill in job_desc.lower():
            skills.append(skill.title())
    
    if not skills:
        skills = ["Communication", "Problem Solving", "Team Collaboration"]
    
    # Create a more sophisticated optimized version
    lines = resume.strip().split('\n')
    optimized_lines = []
    
    for line in lines:
        if 'software engineer' in line.lower():
            optimized_lines.append(line.replace('Software Engineer', 'Senior Software Engineer'))
        elif 'developer' in line.lower():
            optimized_lines.append(line + f" with expertise in {', '.join(skills[:3])}")
        elif line.strip().startswith('•') or line.strip().startswith('-'):
            # Enhance bullet points with relevant keywords
            if any(skill.lower() in line.lower() for skill in skills):
                optimized_lines.append(line + f" (aligned with {skills[0]} requirements)")
            else:
                optimized_lines.append(line)
        else:
            optimized_lines.append(line)
    
    optimized_resume = '\n'.join(optimized_lines)
    
    return {
        "tailored_resume": optimized_resume,
        "key_skills_extracted": skills[:8],
        "optimization_notes": f"Resume optimized to highlight {len(skills)} key skills from the job description. Enhanced job titles, added relevant keywords, and improved bullet points for better ATS compatibility. This demo version provides realistic optimization without requiring AI infrastructure."
    }

def create_resume_optimization_prompt(resume: str, job_desc: str) -> str:
    """
    Create a comprehensive prompt for resume optimization
    """
    return f"""You are an expert Resume Optimizer and ATS (Applicant Tracking System) specialist. Your task is to tailor a resume to match a specific job description while maintaining technical accuracy and authenticity.

**ORIGINAL RESUME:**
{resume}

**TARGET JOB DESCRIPTION:**
{job_desc}

**INSTRUCTIONS:**
1. **Extract Key Skills & Requirements:** Identify the most important technical skills, soft skills, and qualifications from the job description.

2. **Optimize Resume Content:**
   - Rewrite bullet points to mirror the job requirements using similar keywords and phrases
   - Quantify achievements where possible (percentages, numbers, metrics)
   - Ensure technical accuracy - don't add skills the candidate doesn't have
   - Maintain the original structure and format
   - Use action verbs that match the job posting tone

3. **ATS Optimization:**
   - Include relevant keywords naturally throughout the resume
   - Use standard section headings
   - Ensure proper formatting for ATS parsing

4. **Output Format:**
   Please provide your response in the following JSON format:
   {{
     "tailored_resume": "The complete optimized resume text",
     "key_skills_extracted": ["skill1", "skill2", "skill3"],
     "optimization_notes": "Brief explanation of key changes made"
   }}

**IMPORTANT:** Only enhance and optimize existing content. Do not fabricate experience or skills the candidate doesn't possess."""

@app.get("/")
async def root():
    mode = "Demo Mode (No AI Required)" if USE_DEMO_MODE else "AI Mode (Ollama Required)"
    return {"message": f"AI Resume Tailor API is running! - {mode}"}

@app.get("/health")
async def health_check():
    if USE_DEMO_MODE:
        return {"status": "healthy", "model": "demo-mode", "note": "Using mock AI for demonstration"}
    else:
        return {"status": "healthy", "model": MODEL_NAME, "ollama_url": OLLAMA_BASE_URL}

@app.post("/tailor-resume", response_model=ResumeResponse)
async def tailor_resume(request: ResumeRequest):
    """
    Tailor a resume based on job description
    """
    try:
        job_description = request.job_desc
        
        # If job URL is provided, scrape the job description
        if request.job_url:
            try:
                scraped_desc = extract_job_description_from_url(request.job_url)
                if scraped_desc:
                    job_description = scraped_desc
                    logger.info(f"Successfully scraped job description from URL")
            except Exception as e:
                logger.warning(f"Failed to scrape URL, using provided description: {str(e)}")
        
        if USE_DEMO_MODE:
            # Use mock AI optimization
            logger.info("Using mock AI optimization for demo...")
            result = mock_ai_optimization(request.resume, job_description)
            return ResumeResponse(**result)
        else:
            # Use real Ollama API
            prompt = create_resume_optimization_prompt(request.resume, job_description)
            logger.info("Calling Ollama API for resume optimization...")
            response = call_ollama_api(prompt)
            
            # Try to parse JSON response
            try:
                result = json.loads(response)
                return ResumeResponse(**result)
            except json.JSONDecodeError:
                # If not JSON, return as plain text with basic parsing
                return ResumeResponse(
                    tailored_resume=response,
                    key_skills_extracted=["AI/ML", "Python", "Data Analysis"],  # Default
                    optimization_notes="Resume optimized based on job requirements"
                )
            
    except Exception as e:
        logger.error(f"Error in tailor_resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape-job")
async def scrape_job_description(job_url: str):
    """
    Scrape job description from URL
    """
    try:
        job_desc = extract_job_description_from_url(job_url)
        return {"job_description": job_desc}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)