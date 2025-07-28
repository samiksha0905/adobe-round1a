# PDF Outline Extractor

A lightweight, heuristic-based PDF outline extraction tool that detects document titles and heading hierarchies using font size and styling analysis.

## Overview

This tool processes PDF files and extracts their structural outline by analyzing text styling patterns such as font sizes, boldness, and positioning. It's designed to run offline in a Docker container with minimal dependencies.

## Features

- **Title Detection**: Automatically identifies document titles from the largest, topmost text on page 1
- **Heading Hierarchy**: Detects H1, H2, and H3 headings based on font size clustering and styling
- **Heuristic Analysis**: Uses multiple indicators including font size, boldness, whitespace, and text capitalization
- **Multilingual Support**: Preserves Unicode text and works with non-Latin scripts
- **Offline Operation**: No network dependencies, runs completely offline
- **Lightweight**: Uses only PyMuPDF library, total container size < 50 MB

## Architecture

### Components

1. **PDF Loader** (`utils/pdf_loader.py`)
   - Reads PDF files from `/app/input`
   - Handles file discovery and document loading
   - Extracts basic document metadata

2. **Style Extractor** (`utils/style_extractor.py`)
   - Extracts text spans with complete styling information
   - Captures font size, font name, boldness, italics, and positioning
   - Processes all pages and maintains coordinate information

3. **Heading Detector** (`utils/heading_detector.py`)
   - Implements title detection (largest font, topmost position on page 1)
   - Creates font size hierarchy for heading level assignment
   - Applies heuristics for heading validation

4. **Main Driver** (`extract_outline.py`)
   - Orchestrates the extraction pipeline
   - Processes all PDFs in input directory
   - Outputs JSON files with extracted outlines

### Heading Detection Heuristics

The tool uses several heuristics to identify headings:

1. **Font Size Clustering**: Groups similar font sizes and assigns H1 (largest) → H2 → H3
2. **Boldness Requirement**: Prefers bold text for heading detection
3. **Whitespace Analysis**: Looks for extra vertical space above potential headings
4. **Capitalization Patterns**: Recognizes Title Case and ALL CAPS formatting
5. **Position Validation**: Excludes text at very bottom of pages
6. **Text Length**: Filters out very long text blocks

## Installation & Usage

### Building the Docker Image

```bash
# Build for AMD64 platform
docker build --platform linux/amd64 -t outline-extractor:latest .
```

### Running the Container

```bash
# Run with input/output volume mounts
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  outline-extractor:latest
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p input output

# Place PDF files in input/ directory
# Run the extractor
python extract_outline.py
```

## Input/Output Format

### Input
- Place PDF files in the `input/` directory
- Supports any PDF with extractable text

### Output
- JSON files are created in `output/` directory
- Each PDF generates a corresponding `.json` file
- Filename format: `{original_pdf_name}.json`

### JSON Schema

```json
{
  "title": "Document Title",
  "headings": [
    {
      "text": "Heading Text",
      "level": "H1|H2|H3",
      "page": 1
    }
  ],
  "metadata": {
    "page_count": 10,
    "source_file": "example.pdf"
  }
}
```

## Example Output

```json
{
  "title": "Annual Report 2024",
  "headings": [
    {
      "text": "Executive Summary",
      "level": "H1",
      "page": 2
    },
    {
      "text": "Financial Overview",
      "level": "H2",
      "page": 3
    },
    {
      "text": "Revenue Analysis",
      "level": "H3",
      "page": 4
    }
  ],
  "metadata": {
    "page_count": 25,
    "source_file": "annual_report_2024.pdf"
  }
}
```

## Dependencies

- **PyMuPDF** (`fitz`): Fast PDF text extraction and analysis
- **Python 3.10+**: Standard library only

## Performance Characteristics

- **Memory Usage**: < 16 GB RAM for typical documents
- **Processing Speed**: < 5 seconds for 50-page documents on 8-core systems
- **Container Size**: < 50 MB total
- **CPU Usage**: Efficiently utilizes multiple cores

## Limitations

- Works only with PDFs containing extractable text (not scanned images)
- Heuristic-based approach may miss unconventional heading styles
- Limited to 3 heading levels (H1, H2, H3)
- Best results with documents following standard formatting conventions

## Testing

To test with your own PDFs:

1. Place PDF files in the `input/` directory
2. Run the extraction process
3. Check generated JSON files in `output/` directory
4. Verify title and heading detection accuracy

## Troubleshooting

### Common Issues

1. **No text extracted**: PDF may contain only images or be password-protected
2. **Poor heading detection**: Document may use non-standard formatting
3. **Missing title**: Page 1 may not contain a clear title with distinct font size

### Debug Information

The tool provides console output during processing:
- Lists found PDF files
- Shows processing status for each file
- Reports title and heading count
- Displays any errors encountered

## License

This project is designed for educational and research purposes. Please ensure compliance with applicable licenses when using with proprietary PDF content.
