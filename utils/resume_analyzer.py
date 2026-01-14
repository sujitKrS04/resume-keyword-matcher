"""Additional resume analysis features"""

import re
from typing import Dict, List, Tuple
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io


def analyze_resume_length(text: str) -> Dict[str, any]:
    """
    Analyze resume length metrics

    Args:
        text: Resume text

    Returns:
        Dictionary with length metrics and recommendations
    """
    # Count words (excluding whitespace)
    words = text.split()
    word_count = len(words)

    # Count characters
    char_count = len(text)

    # Estimate pages (assuming ~500 words per page)
    estimated_pages = word_count / 500

    # Provide recommendations
    if word_count < 300:
        recommendation = "Too short - Add more details about your experience and skills"
        status = "warning"
    elif word_count < 600:
        recommendation = "Good length - Ideal for 1-page resume"
        status = "success"
    elif word_count < 1000:
        recommendation = (
            "Good length - Suitable for 2-page resume with extensive experience"
        )
        status = "success"
    else:
        recommendation = (
            "Too long - Consider condensing to highlight key achievements only"
        )
        status = "warning"

    return {
        "word_count": word_count,
        "character_count": char_count,
        "estimated_pages": round(estimated_pages, 1),
        "recommendation": recommendation,
        "status": status,
    }


def validate_contact_information(text: str) -> Dict[str, any]:
    """
    Validate presence and format of contact information

    Args:
        text: Resume text

    Returns:
        Dictionary with contact validation results
    """
    results = {
        "email": {"present": False, "valid": False, "value": None},
        "phone": {"present": False, "valid": False, "value": None},
        "linkedin": {"present": False, "value": None},
        "github": {"present": False, "value": None},
        "score": 0,
        "missing": [],
    }

    # Email regex
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    emails = re.findall(email_pattern, text)
    if emails:
        results["email"]["present"] = True
        results["email"]["valid"] = True
        results["email"]["value"] = emails[0]
        results["score"] += 25
    else:
        results["missing"].append("Email")

    # Phone regex (various formats)
    phone_pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    phones = re.findall(phone_pattern, text)
    if phones:
        results["phone"]["present"] = True
        results["phone"]["valid"] = True
        results["phone"]["value"] = (
            phones[0] if isinstance(phones[0], str) else "".join(phones[0])
        )
        results["score"] += 25
    else:
        results["missing"].append("Phone")

    # LinkedIn
    linkedin_patterns = [
        r"linkedin\.com/in/[\w-]+",
        r"LinkedIn:?\s*[\w-]+",
        r"linkedin",
    ]
    for pattern in linkedin_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            results["linkedin"]["present"] = True
            results["score"] += 25
            break
    if not results["linkedin"]["present"]:
        results["missing"].append("LinkedIn")

    # GitHub (bonus)
    github_patterns = [
        r"github\.com/[\w-]+",
        r"GitHub:?\s*[\w-]+",
    ]
    for pattern in github_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            results["github"]["present"] = True
            results["github"]["value"] = match.group()
            results["score"] += 25
            break

    return results


def count_bullet_points(text: str) -> Dict[str, any]:
    """
    Count bullet points in resume

    Args:
        text: Resume text

    Returns:
        Dictionary with bullet point analysis
    """
    # Common bullet point indicators
    bullet_patterns = [
        r"^\s*[•●○■□▪▫–-]\s+",  # Actual bullet symbols
        r"^\s*\*\s+",  # Asterisk
        r"^\s*>\s+",  # Greater than
    ]

    lines = text.split("\n")
    bullet_count = 0
    bullet_lines = []

    for line in lines:
        for pattern in bullet_patterns:
            if re.match(pattern, line):
                bullet_count += 1
                bullet_lines.append(line.strip())
                break

    # Recommendations
    if bullet_count < 5:
        recommendation = "Too few bullet points - Add more specific achievements and responsibilities"
        status = "warning"
    elif bullet_count < 20:
        recommendation = "Good number of bullet points - Well-structured resume"
        status = "success"
    elif bullet_count < 35:
        recommendation = "Adequate bullet points - Consider if all are necessary"
        status = "success"
    else:
        recommendation = "Too many bullet points - Focus on most impactful achievements"
        status = "warning"

    return {
        "total_count": bullet_count,
        "recommendation": recommendation,
        "status": status,
        "sample_bullets": bullet_lines[:5],  # First 5 bullets
    }


def analyze_action_verbs(text: str) -> Dict[str, any]:
    """
    Analyze action verbs in bullet points

    Args:
        text: Resume text

    Returns:
        Dictionary with action verb analysis
    """
    # Strong action verbs
    strong_verbs = {
        "achieved",
        "improved",
        "developed",
        "led",
        "managed",
        "created",
        "designed",
        "implemented",
        "increased",
        "reduced",
        "optimized",
        "streamlined",
        "launched",
        "spearheaded",
        "orchestrated",
        "pioneered",
        "transformed",
        "delivered",
        "executed",
        "built",
        "established",
        "generated",
        "accelerated",
        "enhanced",
        "drove",
        "initiated",
        "innovated",
        "architected",
        "engineered",
        "automated",
        "coordinated",
        "directed",
        "exceeded",
        "maximized",
        "modernized",
        "produced",
        "revamped",
        "scaled",
        "secured",
    }

    # Weak/passive verbs to avoid
    weak_verbs = {
        "responsible",
        "worked",
        "helped",
        "assisted",
        "did",
        "made",
        "got",
        "was",
        "were",
        "had",
        "involved",
        "participated",
        "contributed",
        "handled",
    }

    text_lower = text.lower()
    words = re.findall(r"\b\w+\b", text_lower)

    # Find strong verbs used
    strong_used = [verb for verb in strong_verbs if verb in words]
    strong_count = len(strong_used)

    # Find weak verbs used
    weak_used = [verb for verb in weak_verbs if verb in words]
    weak_count = len(weak_used)

    # Calculate score
    total = strong_count + weak_count
    score = (strong_count / total * 100) if total > 0 else 0

    if score >= 70:
        recommendation = "Excellent use of action verbs!"
        status = "success"
    elif score >= 50:
        recommendation = "Good use of action verbs - Consider replacing some weak verbs"
        status = "success"
    else:
        recommendation = "Replace passive language with strong action verbs"
        status = "warning"

    return {
        "strong_verbs_count": strong_count,
        "weak_verbs_count": weak_count,
        "strong_verbs_used": strong_used[:10],  # Top 10
        "weak_verbs_found": weak_used[:10],
        "score": round(score, 1),
        "recommendation": recommendation,
        "status": status,
    }


def generate_wordcloud(text: str, max_words: int = 50) -> io.BytesIO:
    """
    Generate word cloud from text

    Args:
        text: Text to generate word cloud from
        max_words: Maximum words to include

    Returns:
        BytesIO object containing word cloud image
    """
    # Remove common stop words
    stopwords = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "as",
        "is",
        "was",
        "are",
        "were",
        "been",
        "be",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "should",
        "could",
        "may",
        "might",
        "must",
        "can",
        "this",
        "that",
        "these",
        "those",
    }

    # Create word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        stopwords=stopwords,
        max_words=max_words,
        colormap="viridis",
        relative_scaling=0.5,
        min_font_size=10,
    ).generate(text)

    # Create image
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    plt.tight_layout(pad=0)

    # Save to BytesIO
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", bbox_inches="tight", dpi=100)
    img_buffer.seek(0)
    plt.close()

    return img_buffer


def check_quantification(text: str) -> Dict[str, any]:
    """
    Check for quantified achievements (numbers, percentages, metrics)

    Args:
        text: Resume text

    Returns:
        Dictionary with quantification analysis
    """
    # Patterns for numbers and metrics
    patterns = [
        r"\d+%",  # Percentages
        r"\$\d+[\d,]*[KMB]?",  # Money
        r"\d+[\d,]*\+?\s*(?:users|customers|clients|projects|people|team|members)",  # Counts
        r"\d+[\d,]*\s*(?:hours|days|weeks|months|years)",  # Time
        r"(?:increased|decreased|improved|reduced|grew|saved)\s+(?:by\s+)?\d+",  # Impact metrics
    ]

    all_metrics = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        all_metrics.extend(matches)

    metrics_count = len(all_metrics)

    # Count total bullet points (approximate)
    bullet_count = len(re.findall(r"[•●○■□▪▫–-]\s+", text))

    # Calculate percentage of quantified bullets
    if bullet_count > 0:
        quantified_percentage = (metrics_count / bullet_count) * 100
    else:
        quantified_percentage = 0

    if quantified_percentage >= 60:
        recommendation = "Excellent quantification - Strong evidence of impact"
        status = "success"
    elif quantified_percentage >= 30:
        recommendation = "Good quantification - Consider adding more specific metrics"
        status = "success"
    else:
        recommendation = "Add numbers and metrics to demonstrate your impact"
        status = "warning"

    return {
        "metrics_count": metrics_count,
        "quantified_percentage": round(quantified_percentage, 1),
        "sample_metrics": all_metrics[:10],
        "recommendation": recommendation,
        "status": status,
    }


def calculate_readability_score(text: str) -> Dict[str, any]:
    """
    Calculate readability metrics

    Args:
        text: Resume text

    Returns:
        Dictionary with readability scores
    """
    import textstat

    # Calculate Flesch Reading Ease score
    flesch_score = textstat.flesch_reading_ease(text)

    # Interpret score
    if flesch_score >= 80:
        interpretation = "Very Easy - May be too simple for professional resume"
        recommendation = "Consider using more professional vocabulary"
        status = "warning"
    elif flesch_score >= 60:
        interpretation = "Easy - Good for general audience"
        recommendation = "Perfect balance for most resumes"
        status = "success"
    elif flesch_score >= 50:
        interpretation = "Fairly Difficult - Appropriate for professional resume"
        recommendation = "Good professional tone"
        status = "success"
    elif flesch_score >= 30:
        interpretation = "Difficult - May be too complex"
        recommendation = "Simplify some sentences for better readability"
        status = "warning"
    else:
        interpretation = "Very Difficult - Too complex for resumes"
        recommendation = "Significantly simplify your language"
        status = "warning"

    # Additional metrics
    avg_sentence_length = textstat.avg_sentence_length(text)
    avg_syllables = textstat.avg_syllables_per_word(text)

    return {
        "flesch_score": round(flesch_score, 1),
        "interpretation": interpretation,
        "recommendation": recommendation,
        "status": status,
        "avg_sentence_length": round(avg_sentence_length, 1),
        "avg_syllables": round(avg_syllables, 2),
    }


def create_keyword_density_map(
    text: str, job_description: str = None
) -> Dict[str, any]:
    """
    Analyze keyword frequency and density

    Args:
        text: Resume text
        job_description: Optional job description for comparison

    Returns:
        Dictionary with keyword frequency data
    """
    # Remove common stop words
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "as",
        "is",
        "was",
        "are",
        "were",
        "been",
        "be",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "should",
        "could",
        "may",
        "might",
        "must",
        "can",
        "this",
        "that",
        "these",
        "those",
    }

    # Extract words
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    filtered_words = [word for word in words if word not in stop_words]

    # Count frequency
    word_counts = Counter(filtered_words)
    top_keywords = word_counts.most_common(20)

    # If job description provided, find matching keywords
    matching_keywords = []
    if job_description:
        jd_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", job_description.lower()))
        jd_words = jd_words - stop_words
        matching_keywords = [
            (word, count) for word, count in top_keywords if word in jd_words
        ]

    return {
        "top_keywords": top_keywords,
        "matching_keywords": matching_keywords[:10] if matching_keywords else [],
        "total_words": len(filtered_words),
        "unique_words": len(word_counts),
    }


def export_analysis_to_dict(analysis_result: dict, additional_data: dict) -> dict:
    """
    Prepare analysis data for export to CSV/Excel

    Args:
        analysis_result: Main analysis results
        additional_data: Additional feature results

    Returns:
        Flattened dictionary ready for export
    """
    from datetime import datetime

    export_data = {
        "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "match_score": analysis_result.get("match_score", 0),
        "match_reasoning": analysis_result.get("match_reasoning", ""),
        # Length metrics
        "word_count": additional_data.get("length", {}).get("word_count", 0),
        "estimated_pages": additional_data.get("length", {}).get("estimated_pages", 0),
        # Contact info
        "has_email": additional_data.get("contact", {})
        .get("email", {})
        .get("present", False),
        "has_phone": additional_data.get("contact", {})
        .get("phone", {})
        .get("present", False),
        "has_linkedin": additional_data.get("contact", {})
        .get("linkedin", {})
        .get("present", False),
        "contact_score": additional_data.get("contact", {}).get("score", 0),
        # Bullet points
        "bullet_count": additional_data.get("bullets", {}).get("total_count", 0),
        # Action verbs
        "strong_verbs": additional_data.get("verbs", {}).get("strong_verbs_count", 0),
        "weak_verbs": additional_data.get("verbs", {}).get("weak_verbs_count", 0),
        "verb_score": additional_data.get("verbs", {}).get("score", 0),
        # Quantification
        "metrics_count": additional_data.get("quantification", {}).get(
            "metrics_count", 0
        ),
        "quantified_percentage": additional_data.get("quantification", {}).get(
            "quantified_percentage", 0
        ),
        # Keywords found
        "technical_skills_found": len(
            analysis_result.get("found_keywords", {}).get("technical_skills", [])
        ),
        "soft_skills_found": len(
            analysis_result.get("found_keywords", {}).get("soft_skills", [])
        ),
        # Missing keywords
        "critical_skills_missing": len(
            analysis_result.get("missing_keywords", {}).get(
                "critical_technical_skills", []
            )
        ),
        "soft_skills_missing": len(
            analysis_result.get("missing_keywords", {}).get("important_soft_skills", [])
        ),
    }

    return export_data


def detect_resume_sections(text: str) -> Dict[str, any]:
    """
    Detect and validate resume sections

    Args:
        text: Resume text

    Returns:
        Dictionary with section detection results
    """
    sections_found = {
        "experience": False,
        "education": False,
        "skills": False,
        "summary": False,
        "projects": False,
        "certifications": False,
    }

    section_patterns = {
        "experience": [
            r"\b(work\s+experience|professional\s+experience|employment|experience)\b",
            r"\b(work\s+history|career\s+history)\b",
        ],
        "education": [r"\b(education|academic\s+background|qualifications)\b"],
        "skills": [r"\b(skills|technical\s+skills|core\s+competencies|expertise)\b"],
        "summary": [r"\b(summary|profile|objective|about\s+me)\b"],
        "projects": [r"\b(projects|portfolio|work\s+samples)\b"],
        "certifications": [r"\b(certifications|certificates|licenses)\b"],
    }

    text_lower = text.lower()

    for section, patterns in section_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                sections_found[section] = True
                break

    # Check for required sections
    required = ["experience", "education", "skills"]
    missing_required = [s for s in required if not sections_found[s]]

    if not missing_required:
        status = "success"
        recommendation = "All essential sections present"
    else:
        status = "warning"
        recommendation = f"Missing required sections: {', '.join(missing_required)}"

    return {
        "sections_found": sections_found,
        "missing_required": missing_required,
        "status": status,
        "recommendation": recommendation,
    }


def validate_ats_format(pdf_path: str) -> Dict[str, any]:
    """
    Validate resume for ATS-friendly formatting

    Args:
        pdf_path: Path to PDF file

    Returns:
        Dictionary with ATS validation results
    """
    import pdfplumber

    issues = []
    warnings = []
    metadata = {}

    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract metadata
            if pdf.metadata:
                metadata = {
                    "title": pdf.metadata.get("Title", "Not set"),
                    "author": pdf.metadata.get("Author", "Not set"),
                    "creator": pdf.metadata.get("Creator", "Not set"),
                    "producer": pdf.metadata.get("Producer", "Not set"),
                }

            # Check each page
            has_tables = False
            has_images = False
            has_headers_footers = False
            font_issues = []
            unique_fonts = set()

            for page_num, page in enumerate(pdf.pages, 1):
                # Check for tables
                tables = page.find_tables()
                if tables:
                    has_tables = True
                    issues.append(
                        f"Page {page_num}: Contains tables (ATS may not parse correctly)"
                    )

                # Check for images
                if page.images:
                    has_images = True
                    warnings.append(
                        f"Page {page_num}: Contains {len(page.images)} image(s)"
                    )

                # Check for headers/footers (text in top/bottom 1 inch)
                page_height = page.height
                text_objects = page.extract_words()

                for obj in text_objects:
                    # Check if in header (top 72 points / 1 inch)
                    if obj["top"] < 72:
                        has_headers_footers = True
                    # Check if in footer (bottom 72 points / 1 inch)
                    elif obj["bottom"] > (page_height - 72):
                        has_headers_footers = True

                    # Collect fonts
                    if "fontname" in obj:
                        unique_fonts.add(obj["fontname"])

            # Check fonts
            unusual_fonts = [
                f
                for f in unique_fonts
                if not any(
                    standard in f.lower()
                    for standard in [
                        "arial",
                        "calibri",
                        "times",
                        "helvetica",
                        "georgia",
                        "verdana",
                    ]
                )
            ]

            if unusual_fonts:
                font_issues.extend(unusual_fonts)
                warnings.append(
                    f"Unusual fonts detected: {', '.join(unusual_fonts[:3])}"
                )

            if len(unique_fonts) > 3:
                warnings.append(
                    f"Multiple fonts used ({len(unique_fonts)}). Recommend 1-2 fonts max"
                )

            if has_headers_footers:
                issues.append("Headers/footers detected - ATS may ignore this content")

            # Multi-column detection (approximate)
            if len(pdf.pages) > 0:
                first_page = pdf.pages[0]
                words = first_page.extract_words()
                if words:
                    # Check if text is spread across width (potential columns)
                    x_positions = [w["x0"] for w in words]
                    if len(set(x_positions)) > 50:  # Many different x positions
                        left_side = [w for w in words if w["x0"] < first_page.width / 2]
                        right_side = [
                            w for w in words if w["x0"] >= first_page.width / 2
                        ]
                        if len(left_side) > 10 and len(right_side) > 10:
                            issues.append(
                                "Multi-column layout detected - ATS may read out of order"
                            )

        # Calculate ATS score
        ats_score = 100
        ats_score -= len(issues) * 15  # Major issues
        ats_score -= len(warnings) * 5  # Minor warnings
        ats_score = max(0, min(100, ats_score))

        if ats_score >= 80:
            status = "success"
            overall = "Excellent ATS compatibility"
        elif ats_score >= 60:
            status = "warning"
            overall = "Good ATS compatibility with minor issues"
        else:
            status = "error"
            overall = "Poor ATS compatibility - significant issues found"

        return {
            "ats_score": ats_score,
            "status": status,
            "overall": overall,
            "issues": issues,
            "warnings": warnings,
            "metadata": metadata,
            "has_tables": has_tables,
            "has_images": has_images,
            "has_headers_footers": has_headers_footers,
            "font_count": len(unique_fonts),
            "unusual_fonts": font_issues,
        }

    except Exception as e:
        return {
            "ats_score": 0,
            "status": "error",
            "overall": f"Error analyzing PDF: {str(e)}",
            "issues": [f"Could not analyze PDF: {str(e)}"],
            "warnings": [],
            "metadata": {},
            "has_tables": False,
            "has_images": False,
            "has_headers_footers": False,
            "font_count": 0,
            "unusual_fonts": [],
        }


def check_date_formats(text: str) -> Dict[str, any]:
    """
    Check for inconsistent date formats

    Args:
        text: Resume text

    Returns:
        Dictionary with date format analysis
    """
    # Various date patterns
    date_patterns = {
        "MM/YYYY": r"\b\d{2}/\d{4}\b",
        "Month YYYY": r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b",
        "YYYY-MM": r"\b\d{4}-\d{2}\b",
        "Month, YYYY": r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*, \d{4}\b",
    }

    formats_found = {}
    for format_name, pattern in date_patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            formats_found[format_name] = len(matches)

    if len(formats_found) == 0:
        status = "warning"
        recommendation = "No dates found - consider adding employment/education dates"
    elif len(formats_found) == 1:
        status = "success"
        recommendation = "Consistent date format used throughout"
    else:
        status = "warning"
        recommendation = (
            f"Inconsistent date formats found: {', '.join(formats_found.keys())}"
        )

    return {
        "formats_found": formats_found,
        "format_count": len(formats_found),
        "status": status,
        "recommendation": recommendation,
    }


def find_duplicate_content(text: str) -> Dict[str, any]:
    """
    Find repeated phrases and duplicate content

    Args:
        text: Resume text

    Returns:
        Dictionary with duplicate content analysis
    """
    # Split into sentences
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    # Find exact duplicates
    sentence_counts = Counter(sentences)
    duplicates = [(sent, count) for sent, count in sentence_counts.items() if count > 1]

    # Find similar phrases (5+ words)
    phrases = []
    for sentence in sentences:
        words = sentence.split()
        for i in range(len(words) - 4):
            phrase = " ".join(words[i : i + 5])
            if len(phrase) > 20:
                phrases.append(phrase.lower())

    phrase_counts = Counter(phrases)
    repeated_phrases = [
        (phrase, count) for phrase, count in phrase_counts.items() if count > 1
    ]

    if len(duplicates) == 0 and len(repeated_phrases) == 0:
        status = "success"
        recommendation = "No duplicate content found - good variety"
    elif len(duplicates) > 2 or len(repeated_phrases) > 5:
        status = "warning"
        recommendation = "Significant duplicate content found - vary your descriptions"
    else:
        status = "success"
        recommendation = "Minimal duplication - acceptable"

    return {
        "duplicate_sentences": len(duplicates),
        "repeated_phrases": len(repeated_phrases),
        "duplicates": duplicates[:5],  # Top 5
        "phrases": repeated_phrases[:5],  # Top 5
        "status": status,
        "recommendation": recommendation,
    }
