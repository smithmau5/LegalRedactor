# Legal Doc Redactor

A local Python desktop application designed to identify and redact Personally Identifiable Information (PII) from legal documents (PDF and DOCX) using spaCy and PySide6.

## Features

- **Drag & Drop Interface**: Easily process files by dragging them into the application window.
- **Local PII Detection**: Uses `spaCy` (en_core_web_sm) to identify names, locations, and other sensitive entities locally.
- **Offline Capable**: No data is sent to the cloud. All processing happens on your machine.
- **Format Support**: Handles both PDF and DOCX files.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/flyinknut/LegalDocRedactor.git
   cd LegalDocRedactor
   ```

2. Run the setup script to create a virtual environment and install dependencies:
   ```bash
   chmod +x setup_env.sh
   ./setup_env.sh
   ```

## Usage

1. Start the application:
   ```bash
   ./run_app.sh
   ```

2. Drag PDF or DOCX files into the dropzone.
3. Click "Start Redaction".
4. Redacted files will be saved in the same directory with `_redacted` suffix.

## Requirements

- Python 3.9+
- See `requirements.txt` for full list of dependencies.

## License

MIT License
