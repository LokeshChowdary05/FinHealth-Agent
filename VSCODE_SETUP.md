# VS Code Setup and Run Instructions

## Prerequisites

- Python 3.8 or higher installed
- VS Code installed
- Git installed (optional)

## Step-by-Step Setup in VS Code

### 1. Open Project in VS Code

```powershell
# Navigate to the project directory
cd E:\FinHealth\hospital-price-chatbot

# Open VS Code in current directory
code .
```

### 2. Install Python Extension

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for "Python" by Microsoft
4. Install the Python extension

### 3. Create Virtual Environment

Open VS Code Terminal (`Ctrl+Shift+``) and run:

```powershell
# Create virtual environment
python -m venv env

# Activate virtual environment (Windows PowerShell)
.\env\Scripts\Activate.ps1

# If execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Select Python Interpreter

1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose the interpreter from `.\env\Scripts\python.exe`

### 5. Install Dependencies

In VS Code Terminal:

```powershell
# Make sure virtual environment is activated
# You should see (env) at the beginning of your prompt

pip install -r requirements.txt
```

### 6. Configure Environment Variables

1. Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

2. Edit `.env` file with your API keys:
   - Replace `your_together_ai_api_key_here` with actual Together AI API key
   - Replace `your_openai_api_key_here` with actual OpenAI API key
   - Replace `your_secret_key_here` with a random secret key

### 7. Run the Application

In VS Code Terminal:

```powershell
# Make sure virtual environment is activated
python app.py
```

### 8. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## VS Code Extensions (Recommended)

Install these extensions for better development experience:

1. **Python** (Microsoft) - Already installed
2. **Pylance** (Microsoft) - Enhanced Python support
3. **Python Docstring Generator** - Auto-generate docstrings
4. **Auto Rename Tag** - For HTML editing
5. **Live Server** - For frontend development
6. **GitLens** - Enhanced Git capabilities

## VS Code Launch Configuration

Create `.vscode/launch.json` for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/app.py",
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            },
            "args": [],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

## VS Code Settings

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./env/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "files.associations": {
        "*.html": "html"
    }
}
```

## Development Workflow

### 1. Start Development Server

```powershell
# In VS Code Terminal (make sure env is activated)
python app.py
```

### 2. Debug the Application

1. Set breakpoints in Python files by clicking left of line numbers
2. Press `F5` to start debugging
3. Use Debug Console for interactive debugging

### 3. View Logs

Monitor the VS Code Terminal for:
- Flask server logs
- Error messages
- API request logs

### 4. Live Reload

The Flask development server automatically reloads when you save Python files.

## Project Structure Overview

```
hospital-price-chatbot/
├── app.py                 # Main Flask application
├── medical_analyzer.py    # AI-powered symptom analysis
├── hospital_data.py       # Hospital price comparison logic
├── insurance_analyzer.py  # Insurance coverage analysis
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # Project documentation
├── VSCODE_SETUP.md       # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── styles.css        # CSS styles (black/white theme)
│   └── script.js         # JavaScript interactions
└── data/                 # Data storage directory
```

## Common Commands

### Virtual Environment
```powershell
# Activate
.\env\Scripts\Activate.ps1

# Deactivate
deactivate

# Install new package
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt
```

### Flask Commands
```powershell
# Run development server
python app.py

# Run with custom port
python app.py --port 8000

# Run in production mode
$env:FLASK_ENV="production"; python app.py
```

### Git Commands (if using version control)
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/hospital-price-chatbot.git
git push -u origin main
```

## Troubleshooting

### Common Issues

1. **"python is not recognized"**
   - Make sure Python is installed and added to PATH
   - Try `py` instead of `python`

2. **Virtual environment activation fails**
   - Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

3. **Module not found errors**
   - Make sure virtual environment is activated
   - Verify Python interpreter is set correctly in VS Code

4. **Port already in use**
   - Change port in `app.py` or kill existing process

5. **API errors**
   - Check `.env` file has correct API keys
   - Verify API keys are valid and have proper permissions

### Getting Help

- Check VS Code Python extension documentation
- Flask documentation: https://flask.palletsprojects.com/
- Python debugging in VS Code: https://code.visualstudio.com/docs/python/debugging

## Next Steps

1. Test the basic functionality
2. Add your own API keys for full functionality
3. Customize the hospital data for your region
4. Enhance the AI analysis with better models
5. Add more insurance providers
6. Implement user authentication
7. Add database storage for user data
