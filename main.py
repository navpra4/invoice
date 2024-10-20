import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import re
import cv2
import numpy as np
from pytesseract import Output


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a regular PDF using pdfplumber.
    :param pdf_path: Path to the PDF file
    :return: Extracted text as a string, or None in case of an error
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None


def extract_text_with_confidence(pdf_path):
    """
    Extracts text from a scanned or image-based PDF using OCR (pytesseract),
    and calculates average confidence.
    :param pdf_path: Path to the PDF file
    :return: Extracted text and average confidence score
    """
    try:
        images = convert_from_path(pdf_path)
        full_text = ""
        confidences = []

        for image in images:
            # Convert image to grayscale for better OCR performance
            img_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

            # Perform OCR with detailed output (including confidence scores)
            ocr_data = pytesseract.image_to_data(Image.fromarray(img_gray), output_type=Output.DICT)

            # Extract text and confidence
            for i, word in enumerate(ocr_data['text']):
                if word.strip():  # Ignore empty strings
                    full_text += f"{word} "
                    confidences.append(int(ocr_data['conf'][i]))  # Collect confidence score

        # Calculate average confidence score
        average_confidence = sum(confidences) / len(confidences) if confidences else 0

        return full_text.strip(), average_confidence
    except Exception as e:
        print(f"Error extracting text from scanned PDF with confidence: {e}")
        return None, 0


def extract_text_from_mixed_pdf(pdf_path):
    """
    Attempts to extract text from both regular and image-based PDFs.
    Falls back to OCR if text extraction from pdfplumber is insufficient.
    :param pdf_path: Path to the PDF file
    :return: Extracted text and average confidence score
    """
    extracted_text = extract_text_from_pdf(pdf_path)
    confidence = 100

    if not extracted_text or len(extracted_text) < 100:  # If text extraction fails or is insufficient
        print("Falling back to OCR...")
        extracted_text, confidence = extract_text_with_confidence(pdf_path)

    return extracted_text, confidence


def validate_invoice_data(extracted_text, average_confidence, confidence_threshold=80):
    """
    Validates the extracted invoice data against predefined patterns.
    Also checks for sufficient confidence in OCR results.
    :param extracted_text: Extracted text from the invoice
    :param average_confidence: Average OCR confidence score
    :param confidence_threshold: Threshold for accepting OCR confidence
    :return: Dictionary containing the extracted invoice details and trust status
    """
    # Define regex patterns for invoice details
    invoice_number_pattern = r"Invoice\s*#:\s*(\w+-\d+)"
    date_pattern = r"Invoice Date:\s*([\d]{1,2}\s\w+\s[\d]{4})"
    total_amount_pattern = r"Total\s*₹([\d,]+\.?\d*)"

    # Extract details using regex
    invoice_number_match = re.search(invoice_number_pattern, extracted_text)
    date_match = re.search(date_pattern, extracted_text)
    total_amount_match = re.search(total_amount_pattern, extracted_text)

    # Validate trustworthiness of extracted data
    trusted = True
    if not invoice_number_match:
        print("Invoice number not found!")
        trusted = False

    if not date_match:
        print("Invoice date not found!")
        trusted = False

    if not total_amount_match:
        print("Total amount not found!")
        trusted = False

    if average_confidence < confidence_threshold:
        print(f"Low confidence in OCR results (Confidence: {average_confidence}%)")
        trusted = False

    # Return extracted details and trust status
    return {
        'invoice_number': invoice_number_match.group(1) if invoice_number_match else None,
        'invoice_date': date_match.group(1) if date_match else None,
        'total_amount': total_amount_match.group(1) if total_amount_match else None,
        'trusted': trusted,
        'avg_confidence': average_confidence
    }


if __name__ == "__main__":
    # Example usage
    pdf_path = "/kaggle/input/invoices/INV-150_Bhusan Naresh.pdf"
    
    # Extract text and confidence from the PDF
    extracted_text, avg_confidence = extract_text_from_mixed_pdf(pdf_path)

    # Validate the extracted invoice data
    invoice_data = validate_invoice_data(extracted_text, avg_confidence)
    
    # Print validated invoice data
    print("Validated Invoice Data:", invoice_data)
