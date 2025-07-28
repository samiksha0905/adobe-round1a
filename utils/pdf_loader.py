"""PDF Loader Module

Handles loading and basic processing of PDF files.
"""

import fitz  # PyMuPDF
from typing import List, Dict, Any
import os


class PDFLoader:
    """Loads PDF files and extracts basic document information."""
    
    def __init__(self):
        self.supported_extensions = ['.pdf']
    
    def load_pdf(self, pdf_path: str) -> fitz.Document:
        """
        Load a PDF file and return a PyMuPDF document object.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            fitz.Document: Loaded PDF document
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: If PDF cannot be opened
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            doc = fitz.open(pdf_path)
            return doc
        except Exception as e:
            raise Exception(f"Failed to open PDF {pdf_path}: {str(e)}")
    
    def get_pdf_files(self, input_dir: str) -> List[str]:
        """
        Get all PDF files from the input directory.
        
        Args:
            input_dir: Directory to scan for PDF files
            
        Returns:
            List[str]: List of PDF file paths
        """
        pdf_files = []
        
        if not os.path.exists(input_dir):
            return pdf_files
        
        for filename in os.listdir(input_dir):
            if any(filename.lower().endswith(ext) for ext in self.supported_extensions):
                pdf_files.append(os.path.join(input_dir, filename))
        
        return sorted(pdf_files)
    
    def get_document_info(self, doc: fitz.Document) -> Dict[str, Any]:
        """
        Extract basic document information.
        
        Args:
            doc: PyMuPDF document object
            
        Returns:
            Dict containing document metadata
        """
        metadata = doc.metadata
        return {
            'page_count': doc.page_count,
            'title': metadata.get('title', ''),
            'author': metadata.get('author', ''),
            'subject': metadata.get('subject', ''),
            'creator': metadata.get('creator', ''),
            'producer': metadata.get('producer', ''),
            'creation_date': metadata.get('creationDate', ''),
            'modification_date': metadata.get('modDate', '')
        }
