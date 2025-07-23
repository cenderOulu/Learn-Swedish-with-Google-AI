# Swedish Learning App - Quick Guide

## Installation
1. Install Python 3.8+
2. Install requirements:  
   `pip install google-generativeai python-dotenv tkinter`

## Usage
1. **Start the app**:  
   `python frontend.py`

2. **Main Menu**:
   - Select your CEFR level (A1-A2 to C1-C2)
   - Click "Start" to begin exercises

3. **Exercise Window**:
   - Read the Swedish paragraph
   - Click any word to look it up in Folkets Lexikon
   - Answer multiple-choice questions
   - Use "Next" to advance questions
   - Click "Exit" to return to menu

4. **Settings**:
   - Add/update your Gemini API key
   - Keys are saved in `.env` file

## Troubleshooting
- No API key? Get one from Google AI Studio
- App not responding? Restart and check internet connection
## Building the Application

### Windows Build
```bash
# Install requirements
pip install pyinstaller

# Build with icon
pyinstaller --onefile --windowed --name "Swedish Learn" --icon=assets/icon.ico main.py
### Linux Build
```bash
# Install requirements
pip install pyinstaller

# Build
pyinstaller --onefile --name "swedish-learn" main.py

# The executable will be in dist/ folder