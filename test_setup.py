#!/usr/bin/env python3
"""
Test script for PDF Outline Extractor

This script tests the main functionality with a sample PDF structure.
Run this to verify the installation and basic functionality.
"""

import os
import sys
import json
from pathlib import Path

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.pdf_loader import PDFLoader
from utils.style_extractor import StyleExtractor
from utils.heading_detector import HeadingDetector


def test_components():
    """Test individual components."""
    print("Testing PDF Outline Extractor Components")
    print("=" * 50)
    
    # Test PDF Loader
    try:
        loader = PDFLoader()
        print("✅ PDF Loader initialized successfully")
        
        # Test file discovery
        input_dir = os.path.join(os.path.dirname(__file__), "input")
        os.makedirs(input_dir, exist_ok=True)
        pdf_files = loader.get_pdf_files(input_dir)
        print(f"✅ File discovery working (found {len(pdf_files)} PDFs)")
        
    except Exception as e:
        print(f"❌ PDF Loader error: {e}")
    
    # Test Style Extractor
    try:
        extractor = StyleExtractor()
        print("✅ Style Extractor initialized successfully")
        
        # Test font size analysis
        test_spans = [
            {"font_size": 18.0}, {"font_size": 14.0}, {"font_size": 12.0}
        ]
        sizes = extractor.get_font_sizes(test_spans)
        expected_sizes = [18.0, 14.0, 12.0]
        assert sizes == expected_sizes, f"Expected {expected_sizes}, got {sizes}"
        print("✅ Font size analysis working")
        
    except Exception as e:
        print(f"❌ Style Extractor error: {e}")
    
    # Test Heading Detector
    try:
        detector = HeadingDetector()
        print("✅ Heading Detector initialized successfully")
        
        # Test font hierarchy creation
        test_spans = [
            {"font_size": 18.0, "text": "Title", "page_number": 1, "y": 100},
            {"font_size": 14.0, "text": "Heading 1", "page_number": 1, "y": 200},
            {"font_size": 12.0, "text": "Heading 2", "page_number": 1, "y": 300},
        ]
        hierarchy = detector.create_font_hierarchy(test_spans)
        print(f"✅ Font hierarchy created: {hierarchy}")
        
    except Exception as e:
        print(f"❌ Heading Detector error: {e}")
    
    print("\nComponent testing complete!")


def create_sample_readme():
    """Create a sample README for testing instructions."""
    readme_content = """
# Testing the PDF Outline Extractor

To test this tool with actual PDFs:

1. **Add PDF files to the input directory:**
   ```
   cp your_test_files.pdf input/
   ```

2. **Run the extractor locally:**
   ```bash
   python extract_outline.py
   ```

3. **Or build and run with Docker:**
   ```bash
   # Build the image
   docker build --platform linux/amd64 -t outline-extractor:latest .
   
   # Run the container
   docker run --rm \\
     -v $(pwd)/input:/app/input \\
     -v $(pwd)/output:/app/output \\
     --network none \\
     outline-extractor:latest
   ```

4. **Check the output:**
   - JSON files will be created in the `output/` directory
   - Each PDF will have a corresponding `.json` file with the extracted outline

## Expected Output Format

```json
{
  "title": "Document Title",
  "headings": [
    {
      "text": "Chapter 1: Introduction",
      "level": "H1",
      "page": 2
    },
    {
      "text": "1.1 Overview",
      "level": "H2", 
      "page": 2
    }
  ],
  "metadata": {
    "page_count": 25,
    "source_file": "example.pdf"
  }
}
```

## Testing Tips

- Use PDFs with clear heading hierarchies for best results
- Documents with consistent font sizing work best
- Academic papers, reports, and books typically work well
- Scanned PDFs (images) will not work - only text-based PDFs
"""
    
    with open("TESTING.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("📝 Created TESTING.md with usage instructions")


if __name__ == "__main__":
    test_components()
    create_sample_readme()
    
    print("\n" + "=" * 50)
    print("Setup complete! Next steps:")
    print("1. Add PDF files to the 'input/' directory")
    print("2. Run: python extract_outline.py")
    print("3. Check results in the 'output/' directory")
    print("4. See TESTING.md for detailed instructions")
