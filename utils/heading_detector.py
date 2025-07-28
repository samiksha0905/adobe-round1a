"""Heading Detector Module

Detects document titles and heading hierarchy based on font size and styling.
"""

from typing import List, Dict, Any, Optional, Tuple
import re


class HeadingDetector:
    """Detects titles and headings in PDF documents using heuristic analysis."""
    
    def __init__(self, min_font_size_diff: float = 1.0):
        """
        Initialize the heading detector.
        
        Args:
            min_font_size_diff: Minimum font size difference to consider distinct levels
        """
        self.min_font_size_diff = min_font_size_diff
        self.heading_levels = ["H1", "H2", "H3"]
    
    def detect_title(self, spans: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Detect the document title from page 1 spans.
        
        Args:
            spans: List of text spans from the document
            
        Returns:
            Dictionary containing title information or None
        """
        # Get spans from page 1 only
        page1_spans = [span for span in spans if span["page_number"] == 1]
        
        if not page1_spans:
            return None
        
        # Find the largest font size on page 1
        max_font_size = max(span["font_size"] for span in page1_spans)
        
        # Get all spans with the maximum font size
        title_candidates = [
            span for span in page1_spans 
            if span["font_size"] == max_font_size
        ]
        
        if not title_candidates:
            return None
        
        # If multiple candidates, choose the topmost one (lowest y-value)
        title_span = min(title_candidates, key=lambda x: x["y"])
        
        return {
            "text": title_span["text"],
            "font_size": title_span["font_size"],
            "page_number": title_span["page_number"],
            "position": {"x": title_span["x"], "y": title_span["y"]},
            "is_bold": title_span["is_bold"],
            "is_italic": title_span["is_italic"]
        }
    
    def create_font_hierarchy(self, spans: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Create font size hierarchy for heading detection.
        
        Args:
            spans: List of text spans
            
        Returns:
            Dictionary mapping heading levels to font sizes
        """
        # Get unique font sizes, sorted descending
        unique_sizes = sorted(list(set(span["font_size"] for span in spans)), reverse=True)
        
        # Filter sizes with meaningful differences
        filtered_sizes = []
        for size in unique_sizes:
            if not filtered_sizes or (filtered_sizes[-1] - size) >= self.min_font_size_diff:
                filtered_sizes.append(size)
        
        # Map to heading levels
        hierarchy = {}
        for i, level in enumerate(self.heading_levels):
            if i < len(filtered_sizes):
                hierarchy[level] = filtered_sizes[i]
        
        return hierarchy
    
    def is_likely_heading(self, span: Dict[str, Any], font_hierarchy: Dict[str, float], 
                         prev_span: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[str]]:
        """
        Determine if a span is likely a heading and what level.
        
        Args:
            span: Text span to analyze
            font_hierarchy: Font size hierarchy mapping
            prev_span: Previous span for whitespace analysis
            
        Returns:
            Tuple of (is_heading, heading_level)
        """
        font_size = span["font_size"]
        text = span["text"]
        
        # Check if font size matches any heading level
        heading_level = None
        for level, size in font_hierarchy.items():
            if abs(font_size - size) < 0.1:  # Allow small floating point differences
                heading_level = level
                break
        
        if not heading_level:
            return False, None
        
        # Additional heuristics for heading validation
        
        # 1. Boldness check (prefer bold for headings)
        if not span["is_bold"] and heading_level in ["H1", "H2"]:
            # Be stricter for H1 and H2
            confidence_penalty = True
        else:
            confidence_penalty = False
        
        # 2. Text length check (headings are usually not too long)
        if len(text) > 200:  # Very long text is less likely to be a heading
            return False, None
        
        # 3. Check for title case or all caps (common in headings)
        is_title_case = self._is_title_case(text)
        is_all_caps = text.isupper() and len(text.strip()) > 1
        
        # 4. Whitespace analysis (headings often have space above)
        has_whitespace_above = self._has_significant_whitespace_above(span, prev_span)
        
        # 5. Position check (not at very bottom of page)
        is_reasonable_position = span["y"] < 700  # Rough heuristic for A4 page
        
        # Combine heuristics
        positive_indicators = sum([
            is_title_case,
            is_all_caps,
            has_whitespace_above,
            is_reasonable_position,
            span["is_bold"]
        ])
        
        # Require at least 2 positive indicators for H3, 1 for H1/H2
        min_indicators = 2 if heading_level == "H3" else 1
        
        if confidence_penalty:
            min_indicators += 1
        
        is_heading = positive_indicators >= min_indicators
        
        return is_heading, heading_level if is_heading else None
    
    def _is_title_case(self, text: str) -> bool:
        """Check if text follows title case pattern."""
        if not text:
            return False
        
        words = re.findall(r'\b\w+\b', text)
        if not words:
            return False
        
        # Check if most words start with uppercase
        capitalized_count = sum(1 for word in words if word[0].isupper())
        return capitalized_count / len(words) >= 0.6
    
    def _has_significant_whitespace_above(self, span: Dict[str, Any], 
                                        prev_span: Optional[Dict[str, Any]]) -> bool:
        """Check if there's significant whitespace above the span."""
        if not prev_span:
            return True  # First span on page
        
        # Calculate vertical gap
        gap = span["y"] - (prev_span["y"] + prev_span["height"])
        
        # Consider significant if gap is larger than normal line spacing
        normal_line_spacing = prev_span["height"] * 1.2
        return gap > normal_line_spacing * 1.5
    
    def detect_headings(self, spans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect all headings in the document.
        
        Args:
            spans: List of all text spans from the document
            
        Returns:
            List of detected headings with their information
        """
        if not spans:
            return []
        
        # Create font hierarchy
        font_hierarchy = self.create_font_hierarchy(spans)
        
        if not font_hierarchy:
            return []
        
        headings = []
        
        # Sort spans by page number and y-position
        sorted_spans = sorted(spans, key=lambda x: (x["page_number"], x["y"]))
        
        prev_span = None
        for span in sorted_spans:
            is_heading, level = self.is_likely_heading(span, font_hierarchy, prev_span)
            
            if is_heading and level:
                heading_info = {
                    "text": span["text"],
                    "level": level,
                    "page_number": span["page_number"],
                    "font_size": span["font_size"],
                    "position": {"x": span["x"], "y": span["y"]},
                    "is_bold": span["is_bold"],
                    "is_italic": span["is_italic"]
                }
                headings.append(heading_info)
            
            prev_span = span
        
        return headings
    
    def build_outline(self, headings: List[Dict[str, Any]], title: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Build the final outline structure.
        
        Args:
            headings: List of detected headings
            title: Detected document title
            
        Returns:
            Dictionary containing the complete outline
        """
        outline = {
            "title": title["text"] if title else "",
            "headings": []
        }
        
        for heading in headings:
            heading_entry = {
                "text": heading["text"],
                "level": heading["level"],
                "page": heading["page_number"]
            }
            outline["headings"].append(heading_entry)
        
        return outline
