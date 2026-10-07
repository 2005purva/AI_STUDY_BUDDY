import re
from pypdf import PdfReader

class DocumentProcessor:
    """Handles text extraction from PDFs and plain text files, chunking, and keyword identification."""

    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        """Extracts text content from an uploaded PDF file stream or file path."""
        try:
            reader = PdfReader(pdf_file)
            text_pages = []
            for idx, page in enumerate(reader.pages):
                extracted = page.extract_text()
                if extracted:
                    text_pages.append(f"--- Page {idx + 1} ---\n" + extracted)
            return "\n\n".join(text_pages)
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[dict]:
        """Splits document text into overlapping semantic chunks with metadata."""
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        sentences = re.split(r'(?<=[.!?]) +', cleaned_text)
        
        chunks = []
        current_chunk = []
        current_len = 0
        chunk_id = 0

        for sentence in sentences:
            sentence_len = len(sentence)
            if current_len + sentence_len > chunk_size and current_chunk:
                chunk_str = " ".join(current_chunk)
                chunks.append({
                    "id": chunk_id,
                    "text": chunk_str,
                    "length": len(chunk_str)
                })
                chunk_id += 1
                current_chunk = current_chunk[-1:]
                current_len = sum(len(s) for s in current_chunk)

            current_chunk.append(sentence)
            current_len += sentence_len

        if current_chunk:
            chunk_str = " ".join(current_chunk)
            chunks.append({
                "id": chunk_id,
                "text": chunk_str,
                "length": len(chunk_str)
            })

        return chunks

    @staticmethod
    def extract_key_concepts(text: str, top_n: int = 10) -> list[str]:
        """Extracts key technical terms and concepts from text using word frequency."""
        words = re.findall(r'\b[A-Za-z]{4,}\b', text.lower())
        stopwords = {
            'this', 'that', 'with', 'from', 'have', 'were', 'which', 'their', 'there',
            'about', 'would', 'these', 'other', 'words', 'could', 'write', 'first',
            'water', 'after', 'where', 'called', 'through', 'should', 'between', 'using',
            'page', 'text', 'study', 'note', 'chapter', 'section', 'lecture'
        }
        filtered = [w.capitalize() for w in words if w not in stopwords]
        freq = {}
        for w in filtered:
            freq[w] = freq.get(w, 0) + 1
        
        sorted_concepts = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [concept for concept, count in sorted_concepts[:top_n]]
