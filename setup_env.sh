#!/bin/bash
echo "Setting up LegalDocRedactor Environment..."

# Create venv if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate venv
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo "Downloading spaCy model (en_core_web_sm)..."
python3 -m spacy download en_core_web_sm

echo "Setup complete! Run the app with: ./run_app.sh"
