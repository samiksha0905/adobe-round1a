
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
   docker run --rm \
     -v $(pwd)/input:/app/input \
     -v $(pwd)/output:/app/output \
     --network none \
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
