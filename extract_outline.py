#!/usr/bin/env python3
"""
PDF Outline Extractor

Main script that processes PDF files and extracts document outlines
using heuristic analysis of font sizes and text styling.
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.pdf_loader import PDFLoader
from utils.style_extractor import StyleExtractor
from utils.heading_detector import HeadingDetector


class OutlineExtractor:
    """Main class for extracting outlines from PDF documents."""
    
    def __init__(self):
        self.pdf_loader = PDFLoader()
        self.style_extractor = StyleExtractor()
        self.heading_detector = HeadingDetector()
    
    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract outline from a single PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing the extracted outline
        """
        try:
            # Load PDF document
            doc = self.pdf_loader.load_pdf(pdf_path)
            
            # Extract all text spans with styling information
            spans = self.style_extractor.extract_document_spans(doc)
            
            if not spans:
                return {
                    "title": "",
                    "headings": [],
                    "error": "No text content found in PDF"
                }
            
            # Detect document title
            title = self.heading_detector.detect_title(spans)
            
            # Detect headings
            headings = self.heading_detector.detect_headings(spans)
            
            # Build final outline
            outline = self.heading_detector.build_outline(headings, title)
            
            # Add metadata
            doc_info = self.pdf_loader.get_document_info(doc)
            outline["metadata"] = {
                "page_count": doc_info["page_count"],
                "source_file": os.path.basename(pdf_path)
            }
            
            # Close document
            doc.close()
            
            return outline
            
        except Exception as e:
            return {
                "title": "",
                "headings": [],
                "error": f"Failed to process PDF: {str(e)}",
                "metadata": {
                    "source_file": os.path.basename(pdf_path)
                }
            }
    
    def process_directory(self, input_dir: str, output_dir: str) -> None:
        """
        Process all PDF files in input directory and save outlines to output directory.
        
        Args:
            input_dir: Directory containing PDF files
            output_dir: Directory to save JSON outline files
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all PDF files
        pdf_files = self.pdf_loader.get_pdf_files(input_dir)
        
        if not pdf_files:
            print(f"No PDF files found in {input_dir}")
            return
        
        print(f"Found {len(pdf_files)} PDF file(s) to process:")
        
        # Process each PDF file
        for pdf_path in pdf_files:
            try:
                print(f"Processing: {os.path.basename(pdf_path)}")
                
                # Extract outline
                outline = self.extract_outline(pdf_path)
                
                # Generate output filename
                pdf_filename = os.path.basename(pdf_path)
                output_filename = os.path.splitext(pdf_filename)[0] + ".json"
                output_path = os.path.join(output_dir, output_filename)
                
                # Save outline to JSON file
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(outline, f, indent=2, ensure_ascii=False)
                
                # Print summary
                title = outline.get("title", "No title detected")
                heading_count = len(outline.get("headings", []))
                error = outline.get("error")
                
                if error:
                    print(f"  ❌ Error: {error}")
                else:
                    print(f"  ✅ Title: {title}")
                    print(f"  ✅ Headings found: {heading_count}")
                    
                print(f"  📄 Output saved: {output_filename}")
                print()
                
            except Exception as e:
                print(f"  ❌ Failed to process {pdf_path}: {str(e)}")
                print()


def main():
    """Main entry point for the script."""
    
    # Set up directories
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    # For local development, use current directory structure
    if not os.path.exists(input_dir):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_dir = os.path.join(script_dir, "input")
        output_dir = os.path.join(script_dir, "output")
    
    # Create directories if they don't exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    print("PDF Outline Extractor")
    print("=" * 50)
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Create extractor and process files
    extractor = OutlineExtractor()
    extractor.process_directory(input_dir, output_dir)
    
    print("Processing complete!")


if __name__ == "__main__":
    main()
