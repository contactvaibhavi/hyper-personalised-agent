from abc import ABC, abstractmethod
import logging
import PyPDF2
import pytesseract
from PIL import Image
import fitz
import io
import os
from typing import Type, Dict


# Base parser interface
class BaseParser(ABC):
    @abstractmethod
    def parse(self, filepath: str) -> str:
        """Abstract method to parse file contents."""
        pass


# Concrete Parser for TXT Files
class TxtParser(BaseParser):
    def parse(self, filepath: str) -> str:
        """Parses a text file and returns its contents."""
        try:
            with open(filepath, 'r') as file:
                return file.read()
        except Exception as e:
            logging.error(f"Error reading text file: {e}")
            return "Error reading text file"


class PDFParser(BaseParser):
    def parse(self, filepath: str) -> str:
        try:
            content: str = ""
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if reader.is_encrypted:
                    try:
                        reader.decrypt('')
                    except Exception as e:
                        logging.error(f"Failed to decrypt PDF: {e}")
                        return "Unable to decrypt PDF"
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    page_content = page.extract_text()
                    if not page_content:
                        page_content = self._ocr_page(filepath, page_num)
                    content += page_content
            return content
        except Exception as e:
            logging.error(f"Error processing PDF: {e}")
            return "Error processing PDF File"

    def _ocr_page(self, filepath: str, page_num: int) -> str:
        try:
            document = fitz.open(filepath)
            page = document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img)
            document.close()
            return ocr_text
        except Exception as e:
            logging.error(f"OCR processing error: {e}")
            return "Error in OCR processing"


class ParserFactory:
    _parsers: Dict[str, Type[BaseParser]] = {}

    @classmethod
    def register_parser(cls, extension: str, parser: Type[BaseParser]) -> None:
        cls._parsers[extension] = parser

    @classmethod
    def get_parser(cls, extension: str) -> BaseParser:
        parser = cls._parsers.get(extension)
        if not parser:
            raise ValueError(f"No parser found for extension: {extension}")
        return parser()


ParserFactory.register_parser('txt', TxtParser)
ParserFactory.register_parser('pdf', PDFParser)


class FileParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.parser = self._get_parser()

    def _get_parser(self) -> BaseParser:
        extension = self.filepath.split('.')[-1]
        if extension not in ParserFactory._parsers:
            raise ValueError(f"Unsupported file extension: {extension}")
        return ParserFactory.get_parser(extension)

    def parse(self) -> str:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        return self.parser.parse(self.filepath)
