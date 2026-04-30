import sys
import os

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import subprocess
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = importlib.import_module(package)

def read_docx(file_path):
    install_and_import('docx')
    from docx import Document
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)

def read_pdf(file_path):
    install_and_import('pdfplumber')
    import pdfplumber
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_docs.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        sys.exit(1)
        
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == '.docx':
            content = read_docx(file_path)
            print(content)
        elif ext == '.pdf':
            content = read_pdf(file_path)
            print(content)
        elif ext == '.txt' or ext == '.md':
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print(f"Unsupported file type: {ext}. Only .txt, .md, .docx, and .pdf are supported.")
    except Exception as e:
        print(f"Failed to extract text: {e}")

if __name__ == "__main__":
    main()
