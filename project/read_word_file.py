from docx import Document
def read_word_file(file_path):
    """Read the content of a Word file.

    Args:
        file_path (str): The path of the Word file to read.
        logger (logging.Logger): The logger object to record any errors.

    Returns:
        str or None: The full text content of the Word file, or None if an error occurs.
    """
    try:
        doc = Document(file_path)
        full_text = ""
        for paragraph in doc.paragraphs:
            full_text += paragraph.text + "\n"
        return full_text
    except Exception as e:
        print("Error reading the Word file: "+ f"{e}")
        return None
