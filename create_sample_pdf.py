import fitz  # PyMuPDF

doc = fitz.open()  # new empty PDF
page = doc.new_page()

text = """
CONFIDENTIAL LEGAL DOCUMENT

This document contains sensitive Personally Identifiable Information (PII).

Client Name: Jane Smith
Address: 123 Maple Avenue, Springfield, IL 62704
Social Security Number: 987-65-4321
Date of Birth: January 1, 1980

Witness: John Doe
"""

# Insert text
page.insert_text((50, 50), text, fontsize=12)

doc.save("sample_with_pii.pdf")
print("Created sample_with_pii.pdf")
