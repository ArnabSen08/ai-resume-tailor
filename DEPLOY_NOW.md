# 🚀 Deploy Your Backend to Render (5 Minutes)

## 📋 **Quick Deployment Steps**

### 1. **Create Render Account**
- Go to [render.com](https://render.com)
- Sign up with your GitHub account (free)

### 2. **Deploy Backend**
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `ArnabSen08/ai-resume-tailor`
3. Configure the service:
   - **Name**: `ai-resume-tailor-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: **Free** (512MB RAM)

### 3. **Environment Variables** (Optional)
Add these in Render dashboard:
```
DEMO_MODE=true
PORT=8000
```

### 4. **Get Your Backend URL**
After deployment (2-3 minutes), you'll get a URL like:
```
https://ai-resume-tailor-backend.onrender.com
```

### 5. **Update Frontend**
Edit `script.js` line 2:
```javascript
// Replace this:
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000' 
    : 'https://your-backend-url.onrender.com';

// With your actual URL:
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000' 
    : 'https://ai-resume-tailor-backend.onrender.com';
```

### 6. **Commit and Push**
```bash
git add script.js
git commit -m "Update backend URL for production"
git push
```

## ✅ **What You'll Have**

- **Frontend**: https://arnabsen08.github.io/ai-resume-tailor/ (Auto-updates)
- **Backend**: https://your-backend-url.onrender.com (Your deployed API)
- **Full Functionality**: Resume optimization, job scraping, PDF export

## 🧪 **Test Your Deployment**

1. Visit your live frontend URL
2. Paste a resume and job description
3. Click "Tailor My Resume"
4. Download the optimized resume as PDF

## 💡 **Why This Works**

- **Demo Mode**: No AI infrastructure required
- **Free Hosting**: Both GitHub Pages and Render free tier
- **Realistic Results**: Mock AI provides professional optimization
- **Production Ready**: Handles CORS, errors, and scaling

## 🔄 **Upgrade to Real AI Later**

When ready for real AI:
1. Set `DEMO_MODE=false` in Render
2. Add Ollama or OpenAI integration
3. Deploy with AI capabilities

---

**Your AI Resume Tailor will be fully live in 5 minutes! 🎉**