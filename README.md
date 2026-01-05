# 🤖 AI Resume Tailor

An intelligent resume optimization tool that uses AI to tailor your resume for specific job descriptions. Built with FastAPI backend and vanilla JavaScript frontend.

## 🌟 Features

- **AI-Powered Optimization**: Uses Mistral/Gemma models via Ollama for intelligent resume tailoring
- **File Upload Support**: Upload PDF, DOCX, or TXT resume files for automatic text extraction
- **Web Scraping**: Automatically extract job descriptions from job posting URLs
- **ATS Optimization**: Ensures your resume passes Applicant Tracking Systems
- **PDF Export**: Download your tailored resume as a PDF
- **Real-time Processing**: Fast and responsive AI analysis
- **Free Hosting**: Frontend on GitHub Pages, backend on Render/Railway

## 🚀 Live Demo

- **Frontend**: [https://your-username.github.io/ai-resume-tailor](https://your-username.github.io/ai-resume-tailor)
- **Backend API**: [Your deployed backend URL]

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Responsive design with CSS Grid/Flexbox
- GitHub Pages for hosting

### Backend
- **FastAPI** - Modern Python web framework
- **Ollama** - Local LLM inference
- **BeautifulSoup4** - Web scraping
- **Pydantic** - Data validation
- **ReportLab** - PDF generation

## 📋 Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed locally
- Git and GitHub account

## 🔧 Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-resume-tailor.git
cd ai-resume-tailor
```

### 2. Install Ollama and Models
```bash
# Install Ollama (visit https://ollama.ai for instructions)
# Then pull the required model
ollama pull mistral
# or
ollama pull gemma
```

### 3. Setup Python Backend
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python app.py
```

### 4. Open Frontend
Open `index.html` in your browser or serve it locally:
```bash
# Using Python's built-in server
python -m http.server 3000
```

## 🌐 Deployment

### Frontend (GitHub Pages)
1. Push your code to GitHub
2. Go to repository Settings → Pages
3. Select "Deploy from a branch" → main branch
4. Your frontend will be available at `https://your-username.github.io/ai-resume-tailor`

### Backend (Render - Free Tier)
1. Create account at [Render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python app.py`
6. Add environment variables if needed
7. Update `script.js` with your Render URL

### Backend (Railway - Alternative)
1. Create account at [Railway.app](https://railway.app)
2. Deploy from GitHub
3. Railway auto-detects Python and installs dependencies
4. Update `script.js` with your Railway URL

## 🎯 How It Works

1. **Input**: Upload your resume file (PDF/DOCX/TXT) or paste text, and provide job description (or job URL)
2. **AI Analysis**: The system extracts key requirements from the job posting
3. **Optimization**: AI rewrites your resume to match job requirements while maintaining accuracy
4. **Output**: Get an ATS-optimized resume with highlighted key skills and optimization notes

## 📝 API Endpoints

- `GET /` - Health check
- `GET /health` - Backend status
- `POST /upload-resume` - Upload and extract text from resume files (PDF, DOCX, TXT)
- `POST /tailor-resume` - Main resume optimization endpoint
- `POST /scrape-job` - Extract job description from URL

## 🔒 Environment Variables

For production deployment, set these environment variables:

```bash
OLLAMA_BASE_URL=http://localhost:11434  # Your Ollama instance
MODEL_NAME=mistral                      # AI model to use
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python framework
- [GitHub Pages](https://pages.github.com/) for free frontend hosting

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/your-username/ai-resume-tailor/issues) page
2. Create a new issue with detailed description
3. Contact: [your-email@example.com]

---

**Made with ❤️ by Arnab Sen** | Senior Application Engineer specializing in Big Data & AI