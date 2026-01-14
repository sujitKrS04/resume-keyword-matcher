# 📋 Project Structure & File Overview

Complete overview of the Resume Keyword Matcher project structure.

## 📁 Directory Tree

```
resume-keyword-matcher/
│
├── 📄 app.py                          # Main Streamlit application (1200+ lines)
│   ├── Hero section with animated UI
│   ├── Multi-file upload (up to 3 resumes)
│   ├── Job description input
│   ├── Dual AI provider support (Groq/Gemini)
│   ├── Results visualization (gauges, charts)
│   ├── 14 analysis tabs with comprehensive features
│   ├── PDF report download
│   └── Email integration for report sending
│
├── 📂 utils/                          # Utility modules
│   ├── __init__.py                    # Package initializer
│   ├── pdf_extractor.py               # PDF processing (pdfplumber)
│   │   ├── extract_text_from_pdf()
│   │   ├── validate_pdf()
│   │   └── get_file_info()
│   ├── resume_analyzer.py             # AI integration (Groq + Gemini)
│   │   ├── initialize_groq()
│   │   ├── initialize_gemini()
│   │   ├── analyze_resume_with_ai()
│   │   ├── get_match_rating()
│   │   └── format_keyword_list()
│   ├── report_generator.py            # PDF report generation
│   │   ├── create_analysis_report()
│   │   └── get_rating_for_score()
│   └── email_sender.py                # Email functionality
│       ├── send_analysis_email()
│       └── test_smtp_connection()
│
├── 📂 assets/                         # Static assets
│   ├── styles.css                     # Custom CSS with animations
│   └── images/                        # Image assets (empty, ready for logos)
│
├── 📂 tests/                          # Test suite
│   ├── test_email.py                  # Email testing script
│   └── send_test_email.py             # SMTP connection test
│
├── 📄 requirements.txt                # Python dependencies
├── 📄 .env                            # Environment variables (gitignored)
├── 📄 .gitignore                      # Git ignore rules
│
├── 🚀 setup.py                        # Python setup script
├── 🚀 setup.ps1                       # PowerShell setup script (Windows)
├── 🚀 setup.sh                        # Bash setup script (Unix/Linux/macOS)
│
├── 📖 README.md                       # Main documentation (500+ lines)
├── 📖 QUICKSTART.md                   # Quick setup guide
├── 📖 CONTRIBUTING.md                 # Contribution guidelines
├── 📖 DEPLOYMENT.md                   # Deployment guide (600+ lines)
├── 📖 FEATURES.md                     # Complete features list (300+ lines)
├── 📖 MEDIUM_EASY_FEATURES.md         # Feature implementation guide
├── 📖 PROJECT_COMPLETE.md             # Project completion status
├── 📖 LICENSE                         # MIT License
└── 📖 PROJECT_OVERVIEW.md            # This file
```

## 🎯 File Purposes

### Core Application Files

| File                        | Lines | Purpose                                         |
| --------------------------- | ----- | ----------------------------------------------- |
| `app.py`                    | ~1200 | Main Streamlit app with 14 analysis tabs and UI |
| `utils/pdf_extractor.py`    | ~100  | PDF text extraction and validation              |
| `utils/resume_analyzer.py`  | ~250  | Dual AI integration (Groq + Gemini)             |
| `utils/report_generator.py` | ~250  | PDF report generation with ReportLab            |
| `utils/email_sender.py`     | ~100  | Email sending via SMTP (Gmail support)          |

### Configuration Files

| File               | Purpose                                |
| ------------------ | -------------------------------------- |
| `requirements.txt` | Python package dependencies            |
| `.env`             | Environment variables (API keys, SMTP) |

### Setup & Deployment

| File        | Purpose                            |
| ----------- | ---------------------------------- |
| `setup.py`  | Cross-platform Python setup script |
| `setup.ps1` | Windows PowerShell setup script    |
| `setup.sh`  | Unix/Linux/macOS bash setup script |

### Documentation

| File                      | Lines | Purpose                                |
| ------------------------- | ----- | -------------------------------------- |
| `README.md`               | ~500  | Complete project documentation         |
| `QUICKSTART.md`           | ~150  | Quick setup guide with API key steps   |
| `CONTRIBUTING.md`         | ~200  | Developer contribution guidelines      |
| `DEPLOYMENT.md`           | ~600  | Deployment guide for various platforms |
| `FEATURES.md`             | ~300  | All 18 features detailed list          |
| `MEDIUM_EASY_FEATURES.md` | ~100  | Feature implementation roadmap         |
| `PROJECT_COMPLETE.md`     | ~50   | Project completion checklist           |
| `LICENSE`                 | ~20   | MIT License                            |

### Testing

| File                 | Purpose                             |
| -------------------- | ----------------------------------- |
| `test_email.py`      | Standalone email functionality test |
| `send_test_email.py` | SMTP connection testing script      |

| File                     | Purpose                           |
| ------------------------ | --------------------------------- |
| `tests/conftest.py`      | pytest configuration and fixtures |
| `tests/test_analyzer.py` | Unit tests for analyzer module    |

## 🔧 Key Features by File

### app.py Features

- ✨ Modern glassmorphism UI
- 📊 Interactive Plotly gauge charts
- 🎨 Custom CSS styling
- 📱 Responsive design
- 💾 Session state management
- 📜 Analysis history tracking
- 🎯 Category-wise keyword display
- 📥 PDF report download
- ⚡ Real-time file preview
- 🎨 Color-coded match ratings

### utils/pdf_extractor.py Features

- 📄 PDF text extraction (pdfplumber)
- ✅ File validation (type, size)
- 📊 File info retrieval
- 🔒 Error handling

### utils/gemini_analyzer.py Features

- 🤖 Gemini API integration
- 🔄 Retry logic with exponential backoff
- 📊 JSON response parsing
- 🎯 Structured analysis output
- 🎨 Rating calculation
- 📝 Keyword formatting

### utils/report_generator.py Features

- 📄 Professional PDF generation
- 🎨 Custom styling with ReportLab
- 📊 Structured sections
- 🎯 Category breakdowns
- 📝 Actionable recommendations
- 🤖 ATS tips inclusion

## 📦 Dependencies

### Production Dependencies

```
streamlit==1.29.0           # Web framework
streamlit-extras==0.3.6     # Enhanced components
google-generativeai==0.3.1  # Gemini API client
pdfplumber==0.10.3          # PDF text extraction
plotly==5.18.0              # Interactive charts
python-dotenv==1.0.0        # Environment variables
reportlab==4.0.7            # PDF generation
Pillow==10.1.0              # Image processing
```

### Development Dependencies (Optional)

```
pytest==7.4.3               # Testing framework
black==23.12.0              # Code formatting
flake8==6.1.0               # Linting
mypy==1.7.1                 # Type checking
```

## 🎨 UI Components

### Custom CSS Classes

- `.hero-section` - Gradient hero banner
- `.custom-card` - Glassmorphism cards
- `.score-container` - Score display
- `.keyword-pill` - Keyword badges
- `.step-container` - How-it-works steps
- `.success-box`, `.warning-box`, `.error-box` - Status messages

### Streamlit Components Used

- `st.file_uploader()` - Resume upload
- `st.text_area()` - Job description input
- `st.tabs()` - Category organization
- `st.expander()` - Collapsible sections
- `st.plotly_chart()` - Gauge visualization
- `st.download_button()` - PDF report download
- `st.spinner()` - Loading indicators
- `st.balloons()` - Success animation

## 🔐 Security Features

- ✅ API key encryption (password field)
- ✅ Environment variable management
- ✅ File validation (type, size)
- ✅ Input sanitization
- ✅ XSRF protection enabled
- ✅ No data persistence (privacy)
- ✅ Secrets management for deployment

## 📊 Data Flow

```
User Input (PDF + Job Description)
    ↓
File Validation (pdf_extractor.py)
    ↓
Text Extraction (pdfplumber)
    ↓
API Request (gemini_analyzer.py)
    ↓
Gemini AI Analysis
    ↓
JSON Response Parsing
    ↓
Results Display (app.py)
    ↓
PDF Report Generation (report_generator.py)
    ↓
Download (User)
```

## 🎯 User Journey

1. **Landing** → Hero section with value proposition
2. **Learn** → "How it works" steps
3. **Upload** → PDF resume selection
4. **Input** → Job description paste
5. **Configure** → API key (sidebar)
6. **Analyze** → Click button → Loading spinner
7. **Review** → Match score + visualizations
8. **Explore** → Keywords by category
9. **Improve** → Read recommendations
10. **Download** → PDF report for reference

## 📈 Performance Considerations

### Optimization Techniques

- ✅ Lazy loading of heavy libraries
- ✅ Caching with `@st.cache_data`
- ✅ Efficient PDF parsing
- ✅ Minimal API calls
- ✅ Optimized CSS/JS
- ✅ Compressed assets

### Resource Usage

- **Memory**: ~200-300 MB per session
- **API Calls**: 1 per analysis
- **PDF Size Limit**: 5 MB
- **Response Time**: 10-30 seconds (API dependent)

## 🧪 Testing Coverage

### Implemented Tests

- ✅ Match rating calculation
- ✅ Keyword formatting
- ✅ Edge case handling

### Future Test Plans

- ⏳ PDF extraction validation
- ⏳ API response parsing
- ⏳ Report generation
- ⏳ UI component testing
- ⏳ Integration tests

## 🚀 Deployment Targets

Fully configured for:

- ✅ **Streamlit Cloud** (recommended)
- ✅ **Heroku**
- ✅ **Docker**
- ✅ **AWS EC2**
- ✅ **Google Cloud Run**

## 📝 Documentation Coverage

| Topic               | File              | Status      |
| ------------------- | ----------------- | ----------- |
| Overview & Features | README.md         | ✅ Complete |
| Quick Setup         | QUICKSTART.md     | ✅ Complete |
| Development Guide   | CONTRIBUTING.md   | ✅ Complete |
| Deployment Guide    | DEPLOYMENT.md     | ✅ Complete |
| API Documentation   | Inline docstrings | ✅ Complete |
| Code Comments       | All files         | ✅ Complete |

## 🎨 Color Scheme Reference

### Light Mode

- **Primary**: #6366F1 (Indigo)
- **Secondary**: #8B5CF6 (Purple)
- **Success**: #10B981 (Emerald)
- **Warning**: #F59E0B (Amber)
- **Danger**: #EF4444 (Red)
- **Background**: #F9FAFB (Cool Gray)

### Dark Mode

- **Primary**: #818CF8 (Light Indigo)
- **Secondary**: #A78BFA (Light Purple)
- **Success**: #34D399 (Light Emerald)
- **Warning**: #FBBF24 (Light Amber)
- **Danger**: #F87171 (Light Red)
- **Background**: #0F172A (Slate)

## 🔮 Future Enhancements

Planned features:

- [ ] Multi-language support
- [ ] Word document support (.docx)
- [ ] Resume templates library
- [ ] Comparison mode
- [ ] User accounts
- [ ] Cloud storage
- [ ] Mobile app
- [ ] Browser extension
- [ ] Job board integration

## 📊 Project Statistics

- **Total Files**: 20+
- **Total Lines of Code**: ~2,500+
- **Languages**: Python, CSS, Markdown
- **Documentation**: ~2,000+ lines
- **Setup Scripts**: 3 platforms
- **Test Coverage**: Foundation laid

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup
- Coding standards
- Commit guidelines
- Pull request process

## 📞 Support

- 📖 Documentation in README.md
- 🐛 Report issues on GitHub
- 💬 Discussions for questions
- 📧 Contact maintainers

---

**Built with ❤️ using Streamlit and Google Gemini AI**

Last Updated: January 2026
Version: 1.0.0
