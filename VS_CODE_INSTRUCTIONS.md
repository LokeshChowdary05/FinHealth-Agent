# 🚀 VS Code Instructions for FinHealth Bot

## 📋 Quick Setup Checklist

- [ ] Python 3.8+ installed
- [ ] VS Code installed with Python extension
- [ ] Project downloaded/cloned

## 🔧 Step-by-Step Setup in VS Code

### 1. Open Project in VS Code

```powershell
# Method 1: Command line
cd E:\FinHealth\hospital-price-chatbot
code .

# Method 2: VS Code File menu
# File > Open Folder > Select hospital-price-chatbot folder
```

### 2. Open Integrated Terminal

Press `` Ctrl+` `` (backtick) or:
- View menu > Terminal
- Terminal > New Terminal

### 3. Create and Activate Virtual Environment

```powershell
# Create virtual environment
python -m venv env

# Activate virtual environment (Windows PowerShell)
.\env\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# You should see (env) at the beginning of your terminal prompt
```

### 4. Install Dependencies

```powershell
# Make sure you see (env) in your prompt
pip install -r requirements.txt
```

### 5. Configure Python Interpreter in VS Code

1. Press `Ctrl+Shift+P` to open Command Palette
2. Type "Python: Select Interpreter"
3. Choose the interpreter from `.\env\Scripts\python.exe`

### 6. Set Up Environment Variables

```powershell
# Copy the example environment file
Copy-Item .env.example .env

# Edit .env file (optional - app works without API keys)
# Add your Together AI API key if you have one
```

### 7. Run the Application

```powershell
# Start the Flask development server
python app.py
```

You should see output like:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### 8. Test the Application

1. Open your web browser
2. Navigate to `http://localhost:5000`
3. You should see the FinHealth Bot interface

## 🧪 Testing the Chatbot Features

### Test 1: Symptom Analysis
In the chat interface, type:
```
I have chest pain and shortness of breath
```

Expected response: Analysis of symptoms with recommended procedures

### Test 2: Hospital Price Comparison
```
Compare ECG prices in New York
```

Expected response: Price comparison across multiple hospitals

### Test 3: Insurance Information
```
What insurance plans do you support?
```

Expected response: List of supported insurance plans

### Test 4: General Query
```
How much does an MRI cost?
```

Expected response: MRI pricing information from hospitals

## 🐛 Debugging in VS Code

### Set Breakpoints
1. Click left of line numbers in Python files to set breakpoints
2. Press `F5` to start debugging
3. Select "Python: Flask" configuration

### Debug Console
- Use the Debug Console to inspect variables
- Type expressions to evaluate them

### View Logs
Monitor the VS Code Terminal for:
- Flask server logs
- API request/response data
- Error messages

## 📁 Project Structure Understanding

```
hospital-price-chatbot/
├── 📄 app.py                 # Main Flask application
├── 🧠 medical_analyzer.py    # Symptom analysis logic
├── 🏥 hospital_data.py       # Hospital price comparison
├── 💰 insurance_analyzer.py  # Insurance coverage analysis
├── 📋 requirements.txt       # Python dependencies
├── 🔧 .env                   # Environment variables (create this)
├── 📁 templates/
│   └── 🌐 index.html        # Main web interface
├── 📁 static/
│   ├── 🎨 styles.css        # Styling (black/white theme)
│   └── ⚡ script.js         # JavaScript for interactions
├── 📁 data/
│   └── 📊 hospital_pricing_data.json  # Hospital and pricing data
└── 📁 .vscode/              # VS Code configurations
```

## ⚙️ Development Workflow

### Making Changes

1. **Backend Changes**: Edit Python files (`app.py`, `medical_analyzer.py`, etc.)
   - Flask auto-reloads when you save files
   - Check terminal for any errors

2. **Frontend Changes**: Edit `templates/index.html`, `static/styles.css`, `static/script.js`
   - Refresh browser to see changes
   - Use browser dev tools (`F12`) for debugging

3. **Data Changes**: Edit `data/hospital_pricing_data.json`
   - Restart Flask app to load new data
   - Press `Ctrl+C` in terminal, then `python app.py` again

### Useful VS Code Shortcuts

- `Ctrl+Shift+P`: Command Palette
- `Ctrl+` ` : Toggle Terminal
- `F5`: Start Debugging
- `Ctrl+F5`: Run Without Debugging
- `Ctrl+Shift+F`: Search in Files
- `Ctrl+Shift+E`: Explorer Panel

## 🔍 API Endpoints for Testing

You can test these endpoints using VS Code's REST Client extension or browser:

1. `GET http://localhost:5000/` - Main interface
2. `GET http://localhost:5000/api/health` - Health check
3. `POST http://localhost:5000/api/analyze-symptoms` - Symptom analysis
4. `POST http://localhost:5000/api/compare-hospitals` - Hospital comparison
5. `POST http://localhost:5000/api/chat` - General chat

## 🚨 Common Issues & Solutions

### Issue 1: "python is not recognized"
**Solution:**
```powershell
# Try using 'py' instead of 'python'
py -m venv env
py app.py
```

### Issue 2: Virtual environment activation fails
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\env\Scripts\Activate.ps1
```

### Issue 3: Module not found errors
**Solution:**
```powershell
# Make sure virtual environment is activated (you see (env))
pip install -r requirements.txt
```

### Issue 4: Port 5000 already in use
**Solution:**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID 1234 /F

# Or change port in app.py (last line)
app.run(port=5001)
```

### Issue 5: Empty responses from chatbot
**Solution:**
- Check that `data/hospital_pricing_data.json` exists
- Verify your queries include keywords like "pain", "hospital", "price"
- Check browser console (`F12`) for JavaScript errors

## 💡 Pro Tips

1. **Auto-save**: Enable auto-save in VS Code (File > Auto Save)

2. **Multiple terminals**: Open multiple terminals for different tasks
   - One for running Flask app
   - Another for testing/installing packages

3. **Extensions**: Install these helpful VS Code extensions:
   - Python (Microsoft)
   - Pylance
   - REST Client (for API testing)
   - Live Server (for static files)

4. **Git integration**: Initialize git repository for version control:
   ```powershell
   git init
   git add .
   git commit -m "Initial FinHealth Bot setup"
   ```

5. **Environment isolation**: Always work within the virtual environment to avoid conflicts

## 🎯 Next Steps

After getting the basic setup working:

1. **Customize data**: Edit `data/hospital_pricing_data.json` with your local hospitals
2. **Add API keys**: Get Together AI API key for enhanced symptom analysis
3. **Extend features**: Add more insurance plans or medical procedures
4. **Styling**: Customize the black/white theme in `static/styles.css`
5. **Deploy**: Consider deploying to cloud platforms like Heroku or Azure

## 🆘 Getting Help

If you encounter issues:

1. Check the VS Code terminal for error messages
2. Use browser developer tools (`F12`) to check for JavaScript errors
3. Review the Flask logs in the terminal
4. Ensure all files are saved before testing
5. Try restarting the Flask app (`Ctrl+C`, then `python app.py`)

---

**Happy coding with FinHealth Bot! 🎉**
