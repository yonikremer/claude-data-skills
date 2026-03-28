import sys
from pypdf import PdfReader


def check_fillable_fields(pdf_path: str) -> bool:
    """Checks if a PDF file contains fillable form fields.

    Args:
        pdf_path: The path to the PDF file to check.

    Returns:
        True if the PDF has fillable form fields, False otherwise.
    """
    reader = PdfReader(pdf_path)
    fields = reader.get_fields()
    return bool(fields)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: check_fillable_fields.py [input.pdf]")
        sys.exit(1)

    has_fields = check_fillable_fields(sys.argv[1])
    if has_fields:
        print("This PDF has fillable form fields")
    else:
        print(
            "This PDF does not have fillable form fields; you will need to visually determine where to enter data"
        )
