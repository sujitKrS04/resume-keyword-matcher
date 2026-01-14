"""PDF text extraction utility"""

import io
from typing import Optional
import pdfplumber


def extract_text_from_pdf(pdf_file) -> Optional[str]:
    """
    Extract text content from a PDF file.

    Args:
        pdf_file: Uploaded PDF file (BytesIO or file-like object)

    Returns:
        Extracted text as string, or None if extraction fails
    """
    try:
        # Reset file pointer to beginning
        pdf_file.seek(0)

        text_content = []

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)

        full_text = "\n".join(text_content)

        # Clean up the text
        full_text = full_text.strip()

        return full_text if full_text else None

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None


def validate_pdf(pdf_file, max_size_mb: int = 5) -> tuple[bool, str]:
    """
    Validate PDF file type and size.

    Args:
        pdf_file: Uploaded file
        max_size_mb: Maximum allowed file size in MB

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check file type
        if pdf_file.type != "application/pdf":
            return False, "Please upload a PDF file."

        # Check file size
        pdf_file.seek(0, 2)  # Seek to end
        file_size = pdf_file.tell()
        pdf_file.seek(0)  # Reset to beginning

        max_size_bytes = max_size_mb * 1024 * 1024
        if file_size > max_size_bytes:
            return False, f"File size exceeds {max_size_mb}MB limit."

        return True, ""

    except Exception as e:
        return False, f"Error validating file: {str(e)}"


def get_file_info(pdf_file) -> dict:
    """
    Get basic information about the uploaded PDF.

    Args:
        pdf_file: Uploaded PDF file

    Returns:
        Dictionary with file information
    """
    try:
        pdf_file.seek(0, 2)
        file_size = pdf_file.tell()
        pdf_file.seek(0)

        file_size_mb = file_size / (1024 * 1024)

        return {
            "name": pdf_file.name,
            "size": file_size,
            "size_mb": round(file_size_mb, 2),
        }
    except Exception as e:
        return {"name": "Unknown", "size": 0, "size_mb": 0}
