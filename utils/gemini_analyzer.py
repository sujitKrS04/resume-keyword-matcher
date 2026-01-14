"""AI API integration for resume analysis - Supports Gemini and Groq"""

import os
import json
import re
from typing import Optional, Dict, Any
from google import genai
from google.genai import types
import time


def initialize_gemini(api_key: str):
    """
    Initialize Gemini API with provided key.

    Args:
        api_key: Google Gemini API key
    """
    return genai.Client(api_key=api_key)


def initialize_groq(api_key: str):
    """
    Initialize Groq API with provided key.

    Args:
        api_key: Groq API key
    """
    from groq import Groq

    return Groq(api_key=api_key)


def analyze_resume_with_groq(
    resume_text: str, job_description: str, api_key: str, max_retries: int = 3
) -> Optional[Dict[str, Any]]:
    """
    Analyze resume against job description using Groq API.

    Args:
        resume_text: Extracted text from resume
        job_description: Job description text
        api_key: Groq API key
        max_retries: Maximum number of retry attempts

    Returns:
        Dictionary containing analysis results or None if failed
    """
    try:
        client = initialize_groq(api_key)
        model_id = "llama-3.3-70b-versatile"  # Fast and accurate

        prompt = f"""You are an expert ATS (Applicant Tracking System) and resume analyst. Analyze the following resume against the job description and provide a comprehensive analysis.

Resume:
{resume_text}

Job Description:
{job_description}

Provide your analysis in the following JSON format (respond ONLY with valid JSON, no additional text):
{{
    "match_score": <number between 0-100>,
    "match_reasoning": "<brief explanation of the score>",
    "found_keywords": {{
        "technical_skills": ["skill1", "skill2"],
        "soft_skills": ["skill1", "skill2"],
        "experience_keywords": ["keyword1", "keyword2"],
        "education_keywords": ["keyword1", "keyword2"]
    }},
    "missing_keywords": {{
        "critical_technical_skills": ["skill1", "skill2"],
        "important_soft_skills": ["skill1", "skill2"],
        "experience_gaps": ["gap1", "gap2"],
        "education_gaps": ["gap1", "gap2"]
    }},
    "suggestions": [
        "Specific actionable suggestion 1",
        "Specific actionable suggestion 2",
        "Specific actionable suggestion 3",
        "Specific actionable suggestion 4",
        "Specific actionable suggestion 5"
    ],
    "ats_optimization_tips": [
        "ATS tip 1",
        "ATS tip 2",
        "ATS tip 3"
    ],
    "strengths": [
        "Key strength 1",
        "Key strength 2",
        "Key strength 3"
    ]
}}

Be specific and actionable in your suggestions. Focus on what's actually present or missing in the resume compared to the job description."""

        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=4096,
                )

                if not response or not response.choices:
                    if attempt < max_retries - 1:
                        time.sleep(2**attempt)
                        continue
                    return None

                response_text = response.choices[0].message.content.strip()

                # Extract JSON from response
                json_match = re.search(r"\{[\s\S]*\}", response_text)
                if json_match:
                    json_str = json_match.group()
                    result = json.loads(json_str)

                    # Add match rating
                    result["match_rating"] = get_match_rating(
                        result.get("match_score", 0)
                    )

                    return result
                elif attempt < max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                else:
                    return None

            except Exception as e:
                print(f"Error in Groq API call (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                else:
                    return None

    except Exception as e:
        print(f"Fatal error in Groq analysis: {str(e)}")
        return None


def analyze_resume_with_gemini(
    resume_text: str, job_description: str, api_key: str, max_retries: int = 3
) -> Optional[Dict[str, Any]]:
    """
    Analyze resume against job description using Gemini API.

    Args:
        resume_text: Extracted text from resume
        job_description: Job description text
        api_key: Gemini API key
        max_retries: Maximum number of retry attempts

    Returns:
        Dictionary containing analysis results or None if failed
    """
    try:
        client = initialize_gemini(api_key)
        model_id = "models/gemini-1.5-flash"  # Full model path required

        prompt = f"""You are an expert ATS (Applicant Tracking System) and resume analyst. Analyze the following resume against the job description and provide a comprehensive analysis.

Resume:
{resume_text}

Job Description:
{job_description}

Provide your analysis in the following JSON format (respond ONLY with valid JSON, no additional text):
{{
    "match_score": <number between 0-100>,
    "match_reasoning": "<brief explanation of the score>",
    "found_keywords": {{
        "technical_skills": ["skill1", "skill2"],
        "soft_skills": ["skill1", "skill2"],
        "experience_keywords": ["keyword1", "keyword2"],
        "education_keywords": ["keyword1", "keyword2"]
    }},
    "missing_keywords": {{
        "critical_technical_skills": ["skill1", "skill2"],
        "important_soft_skills": ["skill1", "skill2"],
        "experience_gaps": ["gap1", "gap2"],
        "education_gaps": ["gap1", "gap2"]
    }},
    "suggestions": [
        "Specific actionable suggestion 1",
        "Specific actionable suggestion 2",
        "Specific actionable suggestion 3",
        "Specific actionable suggestion 4",
        "Specific actionable suggestion 5"
    ],
    "ats_optimization_tips": [
        "ATS tip 1",
        "ATS tip 2",
        "ATS tip 3"
    ],
    "strengths": [
        "Key strength 1",
        "Key strength 2",
        "Key strength 3"
    ]
}}

Be specific and actionable in your suggestions. Focus on what's actually present or missing in the resume compared to the job description."""

        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_id, contents=prompt
                )

                if not response or not response.text:
                    if attempt < max_retries - 1:
                        time.sleep(2**attempt)  # Exponential backoff
                        continue
                    return None

                # Extract JSON from response
                response_text = response.text.strip()

                # Try to find JSON in the response (in case there's extra text)
                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    response_text = json_match.group(0)

                analysis_result = json.loads(response_text)

                # Validate the structure
                required_keys = [
                    "match_score",
                    "found_keywords",
                    "missing_keywords",
                    "suggestions",
                ]
                if not all(key in analysis_result for key in required_keys):
                    if attempt < max_retries - 1:
                        time.sleep(2**attempt)
                        continue
                    return None

                # Ensure match_score is within range
                if not isinstance(analysis_result["match_score"], (int, float)):
                    analysis_result["match_score"] = 50

                analysis_result["match_score"] = max(
                    0, min(100, analysis_result["match_score"])
                )

                return analysis_result

            except json.JSONDecodeError as e:
                print(f"JSON decode error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                return None

            except Exception as e:
                print(f"Error in API call (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                return None

        return None

    except Exception as e:
        print(f"Error initializing Gemini or making request: {e}")
        return None


def get_match_rating(score: float) -> tuple[str, str]:
    """
    Get rating category and color based on match score.

    Args:
        score: Match score (0-100)

    Returns:
        Tuple of (rating_text, color)
    """
    if score >= 71:
        return "Excellent Match", "#10B981"  # Green
    elif score >= 41:
        return "Good Match", "#F59E0B"  # Amber
    else:
        return "Needs Improvement", "#EF4444"  # Red


def format_keyword_list(keywords: list) -> str:
    """
    Format a list of keywords for display.

    Args:
        keywords: List of keyword strings

    Returns:
        Formatted string
    """
    if not keywords:
        return "None identified"
    return ", ".join(keywords)
