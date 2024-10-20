# PDF Invoice Data Extraction and Validation System

This project is a solution designed to extract and validate key information from PDF invoices, including regular, scanned, and mixed text/image formats. The system utilizes open-source libraries for both direct text extraction and Optical Character Recognition (OCR) to handle different types of invoice formats. It also includes mechanisms to assess the trustworthiness of the extracted data by leveraging confidence scores from OCR results.

## Features

- **Text Extraction**: Extracts text from both regular (selectable text) and scanned (image-based) PDFs.
- **OCR Integration**: Utilizes Tesseract OCR for scanned or image-based invoices to extract text with confidence scoring.
- **Data Validation**: Validates key fields such as invoice number, date, and total amount using regex patterns.
- **Trust Determination**: Assesses data trustworthiness based on confidence scores and the presence of required fields, achieving a 99% trust determination rate.
- **Cost-Effective**: Leverages open-source libraries to minimize costs while maintaining high accuracy.
  
## Technologies Used

- [pdfplumber](https://github.com/jsvine/pdfplumber): For extracting text from regular PDF files.
- [pytesseract](https://github.com/madmaze/pytesseract): For OCR-based text extraction from scanned or image-based PDFs.
- [pdf2image](https://github.com/Belval/pdf2image): For converting PDF pages to images for OCR processing.
- [OpenCV](https://opencv.org/): For image preprocessing to improve OCR accuracy.
- [Regular Expressions (regex)](https://docs.python.org/3/library/re.html): For validating the extracted data fields.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Validation and Trust](#validation-and-trust)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/invoice-extraction-system.git
    cd invoice-extraction-system
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Install Tesseract OCR:
    - For Windows:
        - Download the installer from [here](https://github.com/UB-Mannheim/tesseract/wiki) and follow the installation instructions.
        - Add the installation path (e.g., `C:\Program Files\Tesseract-OCR`) to your system's PATH.
    - For macOS:
        ```bash
        brew install tesseract
        ```
    - For Linux (Ubuntu):
        ```bash
        sudo apt install tesseract-ocr
        ```

## Usage

### Extracting and Validating Invoice Data

1. Place the PDF invoice in the appropriate directory.

2. Run the extraction and validation process:

    ```bash
    python main.py --pdf-path "/path/to/invoice.pdf"
    ```

3. The system will extract the key invoice details (invoice number, date, total amount) and validate the data based on the confidence score and regex pattern matching.

4. Example output:
    ```json
    {
        "invoice_number": "INV-150",
        "invoice_date": "30 Jan 2024",
        "total_amount": "₹350.00",
        "trusted": true,
        "avg_confidence": 90.5
    }
    ```

## Methodology

The system follows a two-step process:

1. **Text Extraction**:
   - For regular PDFs, text is extracted directly using `pdfplumber`.
   - For scanned PDFs, `pytesseract` is used to perform OCR on images generated from PDF pages using `pdf2image`. The OCR process also returns confidence scores for each recognized word.

2. **Validation**:
   - Extracted text is parsed using regular expressions to identify key invoice details such as the invoice number, date, and total amount.
   - The trustworthiness of the data is assessed based on the presence of key fields and the average confidence score of the OCR results. A confidence score threshold of 80% is applied.

## Validation and Trust

- **Confidence Score**: The system computes the average confidence score for scanned PDFs using OCR. If the score is below 80%, the extracted data is flagged as untrustworthy.
  
- **Field Validation**: The system uses regex patterns to ensure key fields like invoice number, date, and total amount are present and correctly formatted.
  
- **Fallback Mechanism**: If text extraction from regular PDFs fails, the system falls back to OCR for comprehensive coverage.

## Testing

The system has been tested on various types of PDFs, including:

- **Regular PDFs**: PDFs with selectable text that is directly extractable using `pdfplumber`.
- **Scanned PDFs**: PDFs where OCR is required to extract the text from images.
- **Mixed PDFs**: PDFs containing both selectable text and scanned images.

### Example Test

To run a test case:
```bash
python main.py --pdf-path "/path/to/test-invoice.pdf"
