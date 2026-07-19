"""Document loading utilities for PDF, Markdown, and text files."""

import os
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from utils.logger import logger


SUPPORTED_EXTENSIONS = {
    ".pdf": "pypdf",
    ".md": "markdown",
    ".txt": "text",
}


def load_document(file_path: str) -> list[Document]:
    """Load a supported document path into LangChain Document objects."""
    ext = os.path.splitext(file_path)[1].lower()
    logger.info("Loading document: %s (type: %s)", file_path, ext)

    if ext == ".pdf":
        return _load_pdf(file_path)
    if ext == ".md":
        return _load_markdown(file_path)
    if ext == ".txt":
        return _load_text(file_path)

    logger.error("Unsupported file type: %s", ext)
    raise ValueError(f"Unsupported file type: {ext}; only PDF/MD/TXT are supported")


def _load_pdf(file_path: str) -> list[Document]:
    """Load PDF files with PyPDFLoader, one Document per page."""
    logger.info("Loading PDF with PyPDFLoader")
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    logger.info("PDF loaded: pages=%d", len(docs))
    for i, doc in enumerate(docs):
        doc.metadata["page"] = i + 1
        doc.metadata["source_file"] = os.path.basename(file_path)
        doc.metadata["file_type"] = "pdf"
    return docs


def _load_text(file_path: str) -> list[Document]:
    """Load plain text files."""
    logger.info("Loading text with TextLoader")
    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()
    logger.info("Text loaded: documents=%d", len(docs))
    for doc in docs:
        doc.metadata["source_file"] = os.path.basename(file_path)
        doc.metadata["file_type"] = "txt"
    return docs


def _load_markdown(file_path: str) -> list[Document]:
    """Load Markdown as plain text to avoid heavyweight parser side effects."""
    logger.info("Loading Markdown with local text reader")
    content = Path(file_path).read_text(encoding="utf-8")
    return [
        Document(
            page_content=content,
            metadata={
                "source": file_path,
                "source_file": os.path.basename(file_path),
                "file_type": "md",
            },
        )
    ]
