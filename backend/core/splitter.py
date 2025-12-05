def split_text(text: str, chunk_size: int = 800, overlap: int = 100):
    """
    Split text into overlapping chunks.
    - chunk_size: max length of each chunk
    - overlap: repeated characters between chunks for context
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end]
        chunks.append(chunk)

        if end == text_len:
            break

        start = end - overlap

    return chunks