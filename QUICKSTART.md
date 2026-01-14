# 🚀 Quick Start Guide

Get your Resume Keyword Matcher up and running in 5 minutes!

## Prerequisites

- Python 3.13+ installed (or Python 3.9+)
- Groq API key ([Get it free](https://console.groq.com/keys)) - Recommended: 14,400 req/day
- OR Google Gemini API key ([Get it free](https://makersuite.google.com/app/apikey)) - 1,500 req/day
- Optional: Gmail account for email features

## Installation Methods

### Method 1: Automated Setup (Recommended)

#### Windows (PowerShell)

```powershell
# Run the setup script
.\setup.ps1
```

#### macOS/Linux (Bash)

```bash
# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

### Method 2: Manual Setup

1. **Clone and navigate**

```bash
git clone <your-repo-url>
cd resume-keyword-matcher
```

2. **Create virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**

```bash
# Copy the example file (if exists)
cp .env.example .env

# OR create .env file manually
# Add your API keys
```

Edit `.env` file:

```
# Primary AI Provider (Recommended)
GROQ_API_KEY=your_groq_api_key_here

# Optional: Fallback AI Provider
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Email Features
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password_here
```

5. **Run the app**

```bash
streamlit run app.py
```

## Getting Your API Keys

### Groq API (Recommended)

1. Visit [Groq Console](https://console.groq.com/keys)
2. Sign up/Sign in
3. Click "Create API Key"
4. Copy the key (starts with `gsk_`)
5. Add it to your `.env` file

### Google Gemini API (Alternative)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key
5. Add it to your `.env` file

### Gmail SMTP (Optional - for Email Features)

1. Enable 2-Factor Authentication on your Gmail
2. Generate App Password:
   - Google Account → Security → 2-Step Verification → App passwords
3. Select "Mail" and your device
4. Copy the 16-character password
5. Add to `.env` file (remove spaces)

## First Use

1. Open http://localhost:8501 in your browser
2. Select AI provider in sidebar (Groq or Gemini)
3. Enter your API key in the sidebar (if not in .env)
4. Upload 1-3 resume PDFs (max 5MB each)
5. Paste a job description
6. Click "Analyze Resume"
7. Review results across 14 analysis tabs
8. Download PDF report or export to CSV/Excel
9. Optional: Email report from tab 14

## Troubleshooting

### "Module not found" error

```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

### "API key invalid"

- Check for typos in your API key
- Ensure no extra spaces before/after the key
- Verify the key is active in Google AI Studio

### "Could not extract text from PDF"

- Ensure PDF is text-based, not a scanned image
- Try converting the PDF to a newer format
- Use Adobe Acrobat or similar to optimize the PDF

### Port already in use

```bash
# Run on a different port
streamlit run app.py --server.port 8502
```

## Tips for Best Results

1. **Resume**: Use a clean, text-based PDF (not scanned)
2. **Job Description**: Include the full posting with requirements
3. **API Key**: Keep it secure and never commit to version control
4. **Multiple Analyses**: Try different job descriptions for the same resume

## Need Help?

- 📖 Read the full [README.md](README.md)
- 🐛 Report issues on GitHub
- 💬 Check existing issues for solutions

---

**Ready to optimize your resume? Let's go! 🚀**
