"""Style Extractor Module

Extracts text and styling information from PDF pages.
"""

import fitz  # PyMuPDF
from typing import List, Dict, Any, Tuple
import re


class StyleExtractor:
    """Extracts text spans with styling information from PDF pages."""
    
    def __init__(self):
        self.text_spans = []
    
    def extract_page_spans(self, page: fitz.Page) -> List[Dict[str, Any]]:
        """
        Extract all text spans from a PDF page with styling information.
        
        Args:
            page: PyMuPDF page object
            
        Returns:
            List of dictionaries containing span information
        """
        spans = []
        
        # Get text in dictionary format with detailed information
        text_dict = page.get_text("dict")
        
        for block in text_dict["blocks"]:
            if "lines" not in block:  # Skip image blocks
                continue
                
            for line in block["lines"]:
                for span in line["spans"]:
                    # Extract text content
                    text = span["text"].strip()
                    if not text:  # Skip empty spans
                        continue
                    
                    # Extract styling information
                    span_info = {
                        "text": text,
                        "font_size": round(span["size"], 2),
                        "font_name": span["font"],
                        "flags": span["flags"],
                        "bbox": span["bbox"],  # (x0, y0, x1, y1)
                        "x": round(span["bbox"][0], 2),
                        "y": round(span["bbox"][1], 2),
                        "width": round(span["bbox"][2] - span["bbox"][0], 2),
                        "height": round(span["bbox"][3] - span["bbox"][1], 2),
                        "page_number": page.number + 1,  # 1-indexed
                        "is_bold": self._is_bold(span),
                        "is_italic": self._is_italic(span),
                        "color": span.get("color", 0)
                    }
                    
                    spans.append(span_info)
        
        return spans
    
    def _is_bold(self, span: Dict[str, Any]) -> bool:
        """
        Determine if a text span is bold.
        
        Args:
            span: PyMuPDF span dictionary
            
        Returns:
            bool: True if the span is bold
        """
        # Check font name for bold indicators
        font_name = span["font"].lower()
        if any(keyword in font_name for keyword in ["bold", "black", "heavy"]):
            return True
        
        # Check flags (bit 4 = bold)
        return bool(span["flags"] & 2**4)
    
    def _is_italic(self, span: Dict[str, Any]) -> bool:
        """
        Determine if a text span is italic.
        
        Args:
            span: PyMuPDF span dictionary
            
        Returns:
            bool: True if the span is italic
        """
        # Check font name for italic indicators
        font_name = span["font"].lower()
        if any(keyword in font_name for keyword in ["italic", "oblique"]):
            return True
        
        # Check flags (bit 1 = italic)
        return bool(span["flags"] & 2**1)
    
    def extract_document_spans(self, doc: fitz.Document) -> List[Dict[str, Any]]:
        """
        Extract all text spans from entire document.
        
        Args:
            doc: PyMuPDF document object
            
        Returns:
            List of all text spans with styling information
        """
        all_spans = []
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            page_spans = self.extract_page_spans(page)
            all_spans.extend(page_spans)
        
        return all_spans
    
    def get_font_sizes(self, spans: List[Dict[str, Any]]) -> List[float]:
        """
        Get unique font sizes sorted in descending order.
        
        Args:
            spans: List of text spans
            
        Returns:
            List of unique font sizes sorted descending
        """
        sizes = list(set(span["font_size"] for span in spans))
        return sorted(sizes, reverse=True)
    
    def filter_spans_by_page(self, spans: List[Dict[str, Any]], page_number: int) -> List[Dict[str, Any]]:
        """
        Filter spans by page number.
        
        Args:
            spans: List of text spans
            page_number: Page number to filter by (1-indexed)
            
        Returns:
            List of spans from the specified page
        """
        return [span for span in spans if span["page_number"] == page_number]
    
    def is_title_case(self, text: str) -> bool:
        """
        Check if text follows title case pattern.
        
        Args:
            text: Text to check
            
        Returns:
            bool: True if text appears to be in title case
        """
        if not text:
            return False
        
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text)
        if not words:
            return False
        
        # Check if most words start with uppercase
        capitalized_count = sum(1 for word in words if word[0].isupper())
        return capitalized_count / len(words) >= 0.7  # At least 70% capitalized
