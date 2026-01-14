"""Quick test to send an email with analysis"""

import os
from dotenv import load_dotenv
from utils.email_sender import send_analysis_email
from utils.report_generator import create_analysis_report

load_dotenv()

# Sample analysis data
analysis_data = {
    "match_score": 85,
    "match_rating": "Excellent Match",
    "match_reasoning": "Strong technical skills alignment",
    "found_keywords": {
        "technical_skills": ["Python", "JavaScript", "React"],
        "soft_skills": ["Communication", "Leadership"],
    },
    "missing_keywords": {"critical_technical_skills": ["AWS"]},
    "suggestions": ["Add cloud experience", "Highlight project management"],
}

print("Generating PDF...")
pdf_buffer = create_analysis_report(analysis_data, "test_resume.pdf")
pdf_bytes = pdf_buffer.getvalue()
print(f"PDF generated: {len(pdf_bytes)} bytes")

print("\nSending email...")
recipient = "sujitsarkar1604@gmail.com"  # Send to yourself for testing

result = send_analysis_email(recipient, analysis_data, pdf_bytes, "test_resume.pdf")

if result["success"]:
    print(f"\n✅ SUCCESS: {result['message']}")
else:
    print(f"\n❌ ERROR: {result['error']}")
