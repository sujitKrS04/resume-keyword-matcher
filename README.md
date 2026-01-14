# 📄 Resume Keyword Matcher

A modern, AI-powered web application that helps students and job seekers optimize their resumes by comparing them against job descriptions using advanced AI (Groq/Gemini).

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.52.2-FF4B4B.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### Core AI Analysis

- 🤖 **Dual AI Support** - Choose between Groq AI (faster, 14,400 req/day) or Google Gemini
- 📤 **Multi-Resume Upload** - Analyze up to 3 resumes simultaneously with comparison
- 📝 **Smart Matching** - AI-powered resume-job description analysis
- 📊 **Match Score** - 0-100% match score with intelligent rating system
- 🎯 **Keyword Analysis** - Technical skills, soft skills, experience, and education
- 💡 **AI Suggestions** - 5-7 actionable improvement recommendations
- 🏆 **Best Match Selection** - Smart algorithm considers skills and gaps

### Advanced Analysis (14 Tabs)

1. **📏 Length Analysis** - Word, character, page count with recommendations
2. **📧 Contact Validation** - Email, phone, LinkedIn, website verification
3. **📋 Bullet Points** - Bullet usage analysis and suggestions
4. **💪 Action Verbs** - Identifies 50+ strong action verbs
5. **☁️ Word Cloud** - Visual keyword frequency representation
6. **📊 Metrics Checker** - Finds quantifiable achievements
7. **📖 Readability Score** - Flesch-Kincaid, Gunning Fog, SMOG analysis
8. **🔥 Keyword Density** - Heatmap of top keywords
9. **💾 Export** - Download analysis as CSV/Excel
10. **📑 Section Detector** - Identifies resume sections
11. **📅 Date Format** - Validates date consistency
12. **🔄 Duplicate Finder** - Detects repetitive content
13. **🤖 ATS Check** - Validates ATS-friendly formatting
14. **📧 Email Results** - Send PDF reports via email

### Professional Features

- 📥 **PDF Report Generation** - Professional analysis reports
- 📧 **Email Integration** - Send results directly via Gmail/Outlook
- 📈 **Visual Analytics** - Interactive Plotly charts and gauges
- 🎨 **Modern UI** - Professional light theme with sky blue accents
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 📜 **Analysis History** - Session-based history tracking
- 💾 **Export Options** - CSV and Excel export for data analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.13+ (or 3.9+)
- Groq API key ([Get free](https://console.groq.com/keys)) **OR** Gemini API key
- SMTP credentials (optional, for email features)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/resume-keyword-matcher.git
cd resume-keyword-matcher
```

2. **Create a virtual environment**

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

4. **Set up environment variables**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys:
# AI_PROVIDER=groq
# GROQ_API_KEY=your_groq_key_here
# SMTP_EMAIL=your_email@gmail.com (optional)
# SMTP_PASSWORD=your_app_password (optional)
```

5. **Run the application**

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🎯 How to Use

### Step 1: Get API Key

**Groq (Recommended):**

1. Visit [Groq Console](https://console.groq.com/keys)
2. Sign up and create an API key
3. Free tier: 14,400 requests/day, faster responses

**OR Google Gemini:**

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Free tier: 1,500 requests/day

### Step 2: Analyze Resume(s)

1. Enter your Gemini API key in the sidebar
2. Upload your resume (PDF format, max 5MB)
3. Paste the complete job description
4. Click "🚀 Analyze Resume"
5. Wait 10-30 seconds for AI analysis

### Step 3: Review Results

- Check your **overall match score** with visual gauge
- Review **found keywords** by category
- Identify **missing keywords** to add
- Read **actionable recommendations**
- Apply **ATS optimization tips**
- Download your **PDF report**

## 📁 Project Structure

```
resume-keyword-matcher/
├── app.py                          # Main Streamlit application
├── utils/
│   ├── __init__.py                 # Package initializer
│   ├── pdf_extractor.py            # PDF text extraction utilities
│   ├── gemini_analyzer.py          # Gemini API integration
│   └── report_generator.py         # PDF report generation
├── assets/
│   ├── styles.css                  # Custom CSS styles
│   └── images/                     # Image assets
├── .streamlit/
│   ├── config.toml                 # Streamlit configuration
│   └── secrets.toml.example        # Secrets template
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🛠️ Technology Stack

### Core Technologies

- **Framework**: [Streamlit](https://streamlit.io/) 1.29.0
- **AI/NLP**: [Google Gemini API](https://ai.google.dev/) (gemini-pro model)
- **PDF Processing**: [pdfplumber](https://github.com/jsvine/pdfplumber) 0.10.3
- **Language**: Python 3.9+

### Key Libraries

- **streamlit-extras**: Enhanced Streamlit components
- **plotly**: Interactive data visualizations
- **python-dotenv**: Environment variable management
- **reportlab**: PDF report generation
- **google-generativeai**: Gemini API client

## 🎨 Design Features

### Color Scheme

| Purpose   | Light Mode        | Dark Mode               |
| --------- | ----------------- | ----------------------- |
| Primary   | #6366F1 (Indigo)  | #818CF8 (Light Indigo)  |
| Secondary | #8B5CF6 (Purple)  | #A78BFA (Light Purple)  |
| Success   | #10B981 (Emerald) | #34D399 (Light Emerald) |
| Warning   | #F59E0B (Amber)   | #FBBF24 (Light Amber)   |
| Danger    | #EF4444 (Red)     | #F87171 (Light Red)     |

### UI Elements

- ✨ Glassmorphism effects on cards
- 🎨 Gradient borders and backgrounds
- 🎭 Smooth animations and transitions
- 📊 Interactive gauge charts
- 🏷️ Color-coded keyword pills
- 📱 Responsive design with breakpoints

## 📊 Match Score Ratings

| Score Range | Rating            | Color     | Meaning                                |
| ----------- | ----------------- | --------- | -------------------------------------- |
| 71-100%     | Excellent Match   | 🟢 Green  | Strong alignment with job requirements |
| 41-70%      | Good Match        | 🟡 Yellow | Decent fit, room for improvement       |
| 0-40%       | Needs Improvement | 🔴 Red    | Significant gaps, major changes needed |

## 🔐 Security & Privacy

- ✅ API keys stored in environment variables
- ✅ No data stored on servers (client-side processing)
- ✅ File validation and size limits (5MB max)
- ✅ XSRF protection enabled
- ✅ Secure API key input (password field)
- ⚠️ Your resume and job descriptions are sent to Google Gemini API for analysis

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. **Push your code to GitHub**

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/resume-keyword-matcher.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud**

- Go to [share.streamlit.io](https://share.streamlit.io)
- Click "New app"
- Connect your GitHub repository
- Set branch to `main` and main file to `app.py`
- Click "Deploy"

3. **Configure Secrets**

- In Streamlit Cloud dashboard, go to your app settings
- Click "Secrets"
- Add your Gemini API key:

```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

### Deploy to Other Platforms

#### Heroku

```bash
# Add Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
heroku config:set GEMINI_API_KEY=your_key
```

#### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🧪 Testing Checklist

- ✅ Upload various PDF formats (ensure compatibility)
- ✅ Test with different resume lengths (1-5 pages)
- ✅ Verify API error handling and retries
- ✅ Check responsive design on mobile devices
- ✅ Test with empty/invalid inputs
- ✅ Validate match score accuracy
- ✅ Test download report functionality
- ✅ Check analysis history tracking
- ✅ Test with rate-limited API scenarios

## 📝 API Configuration

### Gemini API Limits (Free Tier)

- **Rate Limit**: 60 requests per minute
- **Daily Quota**: Varies by region
- **Token Limit**: ~30,000 tokens per request
- **Model**: gemini-pro

### Error Handling

The app includes robust error handling for:

- Invalid API keys
- Rate limiting (with exponential backoff)
- PDF extraction failures
- Network errors
- Malformed API responses

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
streamlit run app.py --server.runOnSave true

# Format code
black app.py utils/

# Type checking
mypy app.py utils/
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Could not extract text from PDF"

- **Solution**: Ensure your PDF is text-based, not a scanned image. Try using OCR software first.

**Issue**: "API key invalid"

- **Solution**: Double-check your Gemini API key. Ensure there are no extra spaces.

**Issue**: "Analysis failed" or timeout

- **Solution**: You may have hit the rate limit. Wait 60 seconds and try again.

**Issue**: PDF upload rejected

- **Solution**: Ensure file is under 5MB and is a valid PDF format.

**Issue**: Blank analysis results

- **Solution**: Check that both resume and job description have sufficient text content.

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Resume Writing Guide](https://www.indeed.com/career-advice/resumes-cover-letters)
- [ATS-Friendly Resume Tips](https://www.jobscan.co/blog/ats-resume/)
- [Action Verbs for Resumes](https://www.indeed.com/career-advice/resumes-cover-letters/action-verbs-to-make-your-resume-stand-out)

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2026 Resume Keyword Matcher

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Author

Built with ❤️ by [Your Name]

## 🌟 Acknowledgments

- Google Gemini AI for providing the powerful language model
- Streamlit team for the amazing framework
- The open-source community for excellent libraries

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [closed issues](https://github.com/yourusername/resume-keyword-matcher/issues?q=is%3Aissue+is%3Aclosed)
3. Open a [new issue](https://github.com/yourusername/resume-keyword-matcher/issues/new)

## 🗺️ Roadmap

Future enhancements planned:

- [ ] Multi-language support (Spanish, French, German)
- [ ] Support for Word documents (.docx)
- [ ] Resume templates library
- [ ] Comparison mode (compare multiple resumes)
- [ ] Export to multiple formats (Word, JSON)
- [ ] User accounts and cloud storage
- [ ] Browser extension for LinkedIn/Indeed
- [ ] Mobile app (React Native)
- [ ] Integration with job boards
- [ ] Resume builder with AI suggestions

---

**⭐ If you find this project helpful, please consider giving it a star on GitHub!**

Made with 💙 using Streamlit and Google Gemini AI
