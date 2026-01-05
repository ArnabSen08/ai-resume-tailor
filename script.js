// Configuration
const API_BASE_URL = 'http://localhost:8000'; // Change this to your deployed backend URL

// DOM Elements
const resumeTextarea = document.getElementById('resume');
const jobDescTextarea = document.getElementById('jobDesc');
const jobUrlInput = document.getElementById('jobUrl');
const loadingDiv = document.getElementById('loading');
const resultSection = document.getElementById('resultSection');
const errorSection = document.getElementById('errorSection');
const tailoredResumeDiv = document.getElementById('tailoredResume');
const skillsTagsDiv = document.getElementById('skillsTags');
const optimizationNotesDiv = document.getElementById('optimizationNotes');

// Utility Functions
function showLoading() {
    loadingDiv.style.display = 'block';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
}

function hideLoading() {
    loadingDiv.style.display = 'none';
}

function showError(message) {
    errorSection.innerHTML = `<strong>Error:</strong> ${message}`;
    errorSection.style.display = 'block';
    hideLoading();
}

function showResult(data) {
    // Display tailored resume
    tailoredResumeDiv.textContent = data.tailored_resume;
    
    // Display extracted skills
    skillsTagsDiv.innerHTML = '';
    if (data.key_skills_extracted && data.key_skills_extracted.length > 0) {
        data.key_skills_extracted.forEach(skill => {
            const skillTag = document.createElement('span');
            skillTag.className = 'skill-tag';
            skillTag.textContent = skill;
            skillsTagsDiv.appendChild(skillTag);
        });
    }
    
    // Display optimization notes
    optimizationNotesDiv.innerHTML = `<strong>Optimization Notes:</strong> ${data.optimization_notes}`;
    
    resultSection.style.display = 'block';
    hideLoading();
}

// API Functions
async function makeAPIRequest(endpoint, data = null, method = 'GET') {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Unknown error occurred' }));
            throw new Error(errorData.detail || `HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Cannot connect to the backend server. Make sure the API is running.');
        }
        throw error;
    }
}

// Main Functions
async function scrapeJobDescription() {
    const jobUrl = jobUrlInput.value.trim();
    
    if (!jobUrl) {
        showError('Please enter a job URL first.');
        return;
    }
    
    if (!isValidURL(jobUrl)) {
        showError('Please enter a valid URL.');
        return;
    }
    
    showLoading();
    
    try {
        const response = await makeAPIRequest('/scrape-job', { job_url: jobUrl }, 'POST');
        jobDescTextarea.value = response.job_description;
        hideLoading();
        
        // Show success message
        const successMsg = document.createElement('div');
        successMsg.style.cssText = 'background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin: 10px 0; border: 1px solid #c3e6cb;';
        successMsg.textContent = 'Job description extracted successfully!';
        jobUrlInput.parentNode.appendChild(successMsg);
        
        setTimeout(() => successMsg.remove(), 3000);
        
    } catch (error) {
        showError(`Failed to scrape job description: ${error.message}`);
    }
}

async function tailorResume() {
    const resume = resumeTextarea.value.trim();
    const jobDesc = jobDescTextarea.value.trim();
    const jobUrl = jobUrlInput.value.trim();
    
    // Validation
    if (!resume) {
        showError('Please enter your resume.');
        return;
    }
    
    if (!jobDesc && !jobUrl) {
        showError('Please enter a job description or provide a job URL.');
        return;
    }
    
    showLoading();
    
    try {
        const requestData = {
            resume: resume,
            job_desc: jobDesc,
            job_url: jobUrl || null
        };
        
        const response = await makeAPIRequest('/tailor-resume', requestData, 'POST');
        showResult(response);
        
    } catch (error) {
        showError(`Failed to tailor resume: ${error.message}`);
    }
}

function clearAll() {
    resumeTextarea.value = '';
    jobDescTextarea.value = '';
    jobUrlInput.value = '';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    hideLoading();
}

function copyToClipboard() {
    const resumeText = tailoredResumeDiv.textContent;
    
    if (!resumeText) {
        showError('No resume to copy.');
        return;
    }
    
    navigator.clipboard.writeText(resumeText).then(() => {
        // Show success message
        const button = event.target;
        const originalText = button.textContent;
        button.textContent = '✅ Copied!';
        button.style.background = '#27ae60';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '';
        }, 2000);
    }).catch(() => {
        showError('Failed to copy to clipboard.');
    });
}

function downloadAsPDF() {
    const resumeText = tailoredResumeDiv.textContent;
    
    if (!resumeText) {
        showError('No resume to download.');
        return;
    }
    
    // Create a simple PDF using jsPDF (we'll need to include this library)
    // For now, we'll create a formatted text file
    const blob = new Blob([resumeText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'tailored_resume.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    // Show success message
    const button = event.target;
    const originalText = button.textContent;
    button.textContent = '✅ Downloaded!';
    button.style.background = '#27ae60';
    
    setTimeout(() => {
        button.textContent = originalText;
        button.style.background = '';
    }, 2000);
}

// Utility function to validate URL
function isValidURL(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// Auto-resize textareas
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Add event listeners for auto-resize
resumeTextarea.addEventListener('input', () => autoResize(resumeTextarea));
jobDescTextarea.addEventListener('input', () => autoResize(jobDescTextarea));

// Add Enter key support for job URL
jobUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        scrapeJobDescription();
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('AI Resume Tailor loaded successfully!');
    
    // Check if backend is accessible
    makeAPIRequest('/health')
        .then(response => {
            console.log('Backend connection successful:', response);
        })
        .catch(error => {
            console.warn('Backend not accessible:', error.message);
            showError('Backend server is not running. Please start the Python backend first.');
        });
});