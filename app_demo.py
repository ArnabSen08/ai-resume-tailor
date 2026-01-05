from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from typing import Optional, List
import logging

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

def mock_ai_optimization(resume: str, job_desc: str) -> dict:
    """
    Mock AI optimization for demo purposes
    """
    # Extract some keywords from job description
    job_words = job_desc.lower().split()
    skills = []
    
    # Common tech skills to look for
    tech_skills = ['python', 'javascript', 'react', 'fastapi', 'sql', 'aws', 'docker', 'kubernetes', 'machine learning', 'ai', 'data', 'analytics']
    
    for skill in tech_skills:
        if skill in job_desc.lower():
            skills.append(skill.title())
    
    if not skills:
        skills = ["Communication", "Problem Solving", "Team Collaboration"]
    
    # Create a simple optimized version
    optimized_resume = resume.replace("Software Engineer", "Senior Software Engineer")
    optimized_resume = optimized_resume.replace("developer", "developer with expertise in " + ", ".join(skills[:3]))
    
    return {
        "tailored_resume": optimized_resume,
        "key_skills_extracted": skills[:5],
        "optimization_notes": f"Resume optimized to highlight {len(skills)} key skills from the job description. Added relevant keywords and enhanced job titles for better ATS compatibility."
    }

@app.get("/")
async def root():
    return {"message": "AI Resume Tailor API is running! (Demo Mode - No Ollama Required)"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "demo-mode", "note": "Using mock AI for demonstration"}

@app.post("/tailor-resume", response_model=ResumeResponse)
async def tailor_resume(request: ResumeRequest):
    """
    Tailor a resume based on job description (Demo Mode)
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
        
        # Use mock AI optimization
        logger.info("Using mock AI optimization for demo...")
        result = mock_ai_optimization(request.resume, job_description)
        
        return ResumeResponse(**result)
            
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
    uvicorn.run(app, host="0.0.0.0", port=8000)