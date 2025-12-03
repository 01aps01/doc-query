import fitz 

def extract_text_pages(pdf_bytes: bytes):
    
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []

    for i in range(doc.page_count):
        page = doc.load_page(i)
        text = page.get_text("text")
        pages.append({
            "page_no": i + 1,
            "text": text
        })
    return pages
