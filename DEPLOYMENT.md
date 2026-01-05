# 🚀 Deployment Guide

## Overview
Your AI Resume Tailor is now set up with:
- ✅ **Frontend**: GitHub Pages (Free)
- ⏳ **Backend**: Ready for Render/Railway deployment (Free tier)

## 🌐 Live URLs

### Frontend (Already Live!)
**URL**: https://arnabsen08.github.io/ai-resume-tailor/

The frontend is automatically deployed via GitHub Actions whenever you push to the main branch.

### Backend (Next Steps)

## 📋 Backend Deployment Options

### Option 1: Render (Recommended)

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Deploy Backend**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `ArnabSen08/ai-resume-tailor`
   - Configure:
     - **Name**: `ai-resume-tailor-backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
     - **Plan**: Free (512MB RAM, sleeps after 15min inactivity)

3. **Environment Variables** (Optional)
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   MODEL_NAME=mistral
   PORT=8000
   ```

4. **Get Your Backend URL**
   - After deployment, you'll get a URL like: `https://ai-resume-tailor-backend.onrender.com`

### Option 2: Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy**
   - Click "Deploy from GitHub repo"
   - Select `ArnabSen08/ai-resume-tailor`
   - Railway auto-detects Python and deploys

3. **Get Your URL**
   - Railway provides a URL like: `https://ai-resume-tailor-backend.up.railway.app`

## 🔧 Update Frontend Configuration

After deploying your backend, update the frontend:

1. **Edit script.js**
   ```javascript
   // Replace this line in script.js:
   const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
       ? 'http://localhost:8000' 
       : 'https://your-backend-url.onrender.com'; // Replace with your actual URL
   
   // With your actual backend URL:
   const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
       ? 'http://localhost:8000' 
       : 'https://ai-resume-tailor-backend.onrender.com'; // Your actual Render URL
   ```

2. **Commit and Push**
   ```bash
   git add script.js
   git commit -m "Update backend URL for production"
   git push
   ```

3. **Wait for Deployment**
   - GitHub Actions will automatically redeploy your frontend
   - Check the Actions tab in your repository

## 🧪 Testing Your Deployment

### Test Frontend
1. Visit: https://arnabsen08.github.io/ai-resume-tailor/
2. Check if the interface loads correctly

### Test Backend Connection
1. Open browser developer tools (F12)
2. Check console for any connection errors
3. Try the "Extract Job Description" feature with a job URL

### Test Full Workflow
1. Visit: https://arnabsen08.github.io/ai-resume-tailor/
2. **Upload a resume file** (PDF, DOCX, or TXT) OR paste resume text
3. Add a job description or job URL
4. Click "Tailor My Resume"
5. Verify AI response and PDF download

## 🔍 Troubleshooting

### Common Issues

**Backend Not Responding**
- Check if your Render/Railway service is running
- Verify the URL in script.js matches your deployed backend
- Check backend logs in Render/Railway dashboard

**CORS Errors**
- The backend is configured to allow all origins
- If issues persist, update CORS settings in app.py

**Ollama Model Issues**
- Free hosting services don't support Ollama
- Consider using OpenAI API or Hugging Face Inference API
- Update the backend to use cloud-based LLM services

### Alternative: Cloud LLM Integration

If you want to use cloud-based LLMs instead of Ollama:

1. **OpenAI Integration**
   ```python
   # Add to requirements.txt
   openai==1.3.0
   
   # Update app.py to use OpenAI API
   import openai
   openai.api_key = "your-api-key"
   ```

2. **Hugging Face Integration**
   ```python
   # Add to requirements.txt
   transformers==4.35.0
   
   # Use Hugging Face Inference API
   ```

## 📊 Monitoring

### GitHub Pages
- Monitor deployments in: Repository → Actions
- Check status at: Repository → Settings → Pages

### Backend (Render)
- View logs in Render dashboard
- Monitor uptime and performance
- Free tier sleeps after 15min inactivity

### Backend (Railway)
- Check deployment logs in Railway dashboard
- Monitor resource usage
- Free tier has monthly usage limits

## 🔄 Updates and Maintenance

### Updating Code
```bash
# Make changes to your code
git add .
git commit -m "Your update message"
git push

# Frontend updates automatically via GitHub Actions
# Backend updates automatically on Render/Railway
```

### Monitoring Costs
- GitHub Pages: Always free for public repos
- Render Free Tier: 512MB RAM, sleeps after 15min
- Railway Free Tier: $5 credit monthly

## 🎯 Next Steps

1. **Deploy Backend** using Render or Railway
2. **Update script.js** with your backend URL
3. **Test Full Application** end-to-end
4. **Share Your Project** with the community!

## 📞 Support

If you encounter issues:
1. Check the repository Issues tab
2. Review deployment logs
3. Test locally first to isolate the problem

---

**Your AI Resume Tailor is ready to help optimize resumes! 🚀**