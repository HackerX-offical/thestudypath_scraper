# Study Path Scraper

## Overview

This Python script is designed to scrape educational content from The Study Path website, specifically targeting RS Aggarwal Solutions for Class 9, Chapter 15: Volume and Surface Area of Solids. The scraper extracts exercise images and compiles them into organized PDF documents for offline study purposes.

## Features

- **Automated Scraping**: Extracts all exercise pages (15A, 15B, 15C, 15D) and Multiple Choice Questions (MCQs) from the specified chapter.
- **Image Extraction**: Downloads high-quality images of mathematical problems and solutions.
- **PDF Generation**: Converts downloaded images into well-formatted PDF documents.
- **Organized Output**: Creates a structured directory with separate folders for images and PDFs.
- **Error Handling**: Robust error handling for network requests and file operations.
- **Concurrent Processing**: Utilizes concurrent futures for efficient downloading of multiple images.

## Requirements

- Python 3.7+
- Required Python packages:
  - `requests`
  - `beautifulsoup4`
  - `Pillow`

## Installation

1. **Clone or Download**: Ensure you have the script file (`main.py`) in your project directory.

2. **Set up Virtual Environment** (Recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install requests beautifulsoup4 Pillow
   ```

## Usage

1. **Run the Script**:

   ```bash
   python main.py
   ```

   The script will automatically:
   - Install any missing dependencies
   - Scrape the main chapter page
   - Identify and download exercise pages
   - Extract and download all relevant images
   - Generate PDF files for each exercise
   - Clean up temporary image files

2. **Output Structure**:
   ```
   study_path_chapter_15/
   ├── images/          # Temporary image storage (cleaned up after PDF creation)
   ├── pdfs/            # Final PDF documents
   │   ├── Exercise_15A.pdf
   │   ├── Exercise_15B.pdf
   │   ├── Exercise_15C.pdf
   │   ├── Exercise_15D.pdf
   │   └── MCQs.pdf
   └── readme.md        # This file
   ```

## How It Works

1. **Page Discovery**: The script starts by parsing the main chapter page to find links to individual exercise pages.
2. **Image Extraction**: For each exercise page, it identifies and downloads all mathematical content images.
3. **PDF Compilation**: Images are processed and combined into PDF format using Pillow's image handling capabilities.
4. **Cleanup**: Temporary image files are removed after successful PDF creation to save disk space.

## Important Notes

- This tool is intended for educational purposes only.
- Respect website terms of service and avoid overloading servers with excessive requests.
- The script includes appropriate delays and headers to minimize impact on the source website.
- Internet connection is required for scraping and downloading content.

## Troubleshooting

- **ModuleNotFoundError**: Ensure all required packages are installed in your Python environment.
- **Network Errors**: Check your internet connection and try again later.
- **Permission Errors**: Ensure write permissions in the output directory.
- **Incomplete Downloads**: The script is designed to be resilient; re-run if interrupted.

## Author

**Suryanshu Nabheet**

## Ethics

Use only on systems and content you are **authorized** to access. See [SECURITY.md](./SECURITY.md).

## License

Licensed under the [HackerX License](./LICENSE). Redistributions must retain copyright,
license text, and [NOTICE](./NOTICE) attribution per the license terms.
