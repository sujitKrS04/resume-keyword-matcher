# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Multi-language support (Spanish, French, German)
- Support for Word documents (.docx)
- Resume templates library
- User authentication and accounts
- Cloud storage for analysis history
- Mobile app version
- Browser extension

## [3.0.0] - 2025-01-15

### Added - Major Update

- **Dual AI Provider Support**:

  - Groq AI integration (llama-3.3-70b-versatile) as primary provider
  - 14,400 requests/day free tier
  - Faster response times and higher quality analysis
  - Google Gemini as fallback option
  - AI provider selection in sidebar

- **Multi-Resume Comparison**:

  - Upload up to 3 resumes simultaneously
  - Side-by-side comparison table
  - Smart Best Match algorithm considering:
    - Match scores
    - Technical and soft skills alignment
    - Missing critical skills
    - Intelligent ranking system

- **Email Integration** (Tab 14):

  - Send complete analysis reports via email
  - PDF attachment generation
  - Test SMTP connection button
  - Gmail support with app passwords
  - Real-time progress indicators
  - Status messages with session state persistence
  - Callback pattern for reliable sending

- **New Analysis Features**:
  - ATS (Applicant Tracking System) Checker (Tab 12)
    - File format validation
    - Keyword presence check
    - Contact information validation
    - Section structure analysis
    - Overall ATS compatibility score (0-100%)
  - Custom Keyword Suggestions (Tab 13)
    - AI-powered recommendations
    - Technical skills suggestions
    - Industry-specific terms
    - Soft skills recommendations
    - Action verbs to use

### Changed

- Upgraded to Python 3.13+ (compatible with 3.9+)
- Updated Streamlit to 1.52.2
- Reorganized into 14 analysis tabs (from 12)
- Enhanced UI with better navigation
- Improved session state management
- Better error handling and user feedback
- Enhanced PDF report generation
- Updated all documentation files

### Technical Improvements

- Added `utils/email_sender.py` module
- Implemented button callback pattern for email functionality
- Enhanced session state for multi-resume analysis
- Better API error handling and retry logic
- Improved memory management for multiple resumes

## [2.0.0] - 2026-01-12 (Previous Release)

### Added

- Resume Length Checker with word/character/page counts
- Contact Information Validator
- Bullet Point Analysis
- Action Verb Analyzer
- Word Cloud Generator
- Quantification Checker
- Readability Score calculator
- Keyword Density Heatmap
- CSV/Excel export functionality
- Section Detector
- Date Format Checker
- Duplicate Content Finder
- 12 analysis tabs total

## [1.0.0] - 2026-01-12

### Added

- Initial release of Resume Keyword Matcher
- PDF resume upload with validation (max 5MB)
- Job description text input
- AI-powered analysis using Google Gemini API
- Match score calculation (0-100%)
- Keyword extraction by category (technical, soft skills, experience, education)
- Missing keywords identification
- Actionable improvement suggestions
- ATS optimization tips
- Visual gauge charts for match scores
- Color-coded ratings (green, yellow, red)
- PDF report generation and download
- Analysis history tracking (last 3 sessions)
- Modern glassmorphism UI design
- Responsive design for mobile/desktop
- Custom CSS styling with animations
- Dark mode support
- Interactive tooltips and expandable sections
- Sidebar with resume tips and resources
- Error handling with user-friendly messages
- Retry logic for API calls
- Environment variable management
- Multiple setup scripts (Python, PowerShell, Bash)

### Documentation

- Comprehensive README with setup instructions
- Quick start guide (QUICKSTART.md)
- Contributing guidelines (CONTRIBUTING.md)
- Deployment guide for multiple platforms (DEPLOYMENT.md)
- Project overview and structure (PROJECT_OVERVIEW.md)
- MIT License
- Example configuration files

### Technical

- Streamlit 1.29.0 framework
- Google Gemini Pro API integration
- pdfplumber for PDF text extraction
- Plotly for data visualizations
- ReportLab for PDF generation
- python-dotenv for environment management
- Full test suite foundation with pytest

### Deployment Support

- Streamlit Cloud ready
- Heroku configuration
- Docker support with Dockerfile
- AWS EC2 instructions
- Google Cloud Run support

### Security

- API key encryption
- Environment variable management
- File validation and sanitization
- XSRF protection
- No data persistence (privacy-focused)

## [0.9.0] - 2026-01-10 (Beta)

### Added

- Core functionality prototype
- Basic PDF upload
- Simple text analysis
- Match score calculation

### Changed

- Improved UI design
- Enhanced error handling

## [0.5.0] - 2026-01-05 (Alpha)

### Added

- Initial project setup
- Basic Streamlit app structure
- PDF extraction utility
- Gemini API integration

---

## Version History

- **1.0.0** - Full production release
- **0.9.0** - Beta testing version
- **0.5.0** - Alpha development version

## How to Use This Changelog

### For Developers

- Document all changes in the [Unreleased] section
- Move changes to a new version section upon release
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Link to relevant issues/PRs

### Change Categories

- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security fixes

### Example Entry

```markdown
## [1.1.0] - 2026-02-15

### Added

- Support for Word documents (.docx) (#42)
- Resume comparison mode (#45)

### Changed

- Improved PDF extraction speed by 30% (#48)
- Updated UI color scheme (#50)

### Fixed

- Fixed API timeout issue (#44)
- Corrected match score rounding (#47)
```

---

[Unreleased]: https://github.com/yourusername/resume-keyword-matcher/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/resume-keyword-matcher/releases/tag/v1.0.0
[0.9.0]: https://github.com/yourusername/resume-keyword-matcher/releases/tag/v0.9.0
[0.5.0]: https://github.com/yourusername/resume-keyword-matcher/releases/tag/v0.5.0
