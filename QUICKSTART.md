# 🚀 TextPal - Smart Reading Assistant - Quick Start Guide

Welcome! Your complete Smart Reading Assistant (TextPal) project is now ready. This guide will help you get started immediately.

## 📊 Project Overview

**TextPal** is a full-stack web application that helps users improve reading comprehension and accessibility through:
- 📄 PDF/TXT file upload and extraction
- 🔊 Text-to-Speech functionality
- 📝 AI-powered text summarization
- 📊 Reading difficulty analysis (Flesch Reading Ease)
- 🌐 Multi-language translation (English ↔ Tamil)
- 💬 AI chatbot for document Q&A
- 🎨 Customizable fonts & dark mode

## 📁 Project Structure

```
smart_textpal/
├── app.py                      # Flask backend
├── config.py                   # Configuration management
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── setup.py                    # Quick setup script
├── test_textpal.py            # Test suite
│
├── templates/
│   └── index.html             # Main web interface
│
├── static/
│   ├── css/
│   │   └── style.css          # Complete styling (responsive + dark mode)
│   └── js/
│       └── main.js            # Frontend functionality
│
├── utils/
│   ├── __init__.py
│   ├── text_extraction.py     # PDF/TXT parsing
│   ├── text_processing.py     # Summarization, difficulty analysis
│   ├── translation.py         # Multi-language translation
│   └── chatbot.py             # Q&A chatbot
│
├── uploads/                    # User file storage
│
├── README.md                   # Full documentation
├── CONTRIBUTING.md            # Contribution guidelines
├── .env.example               # Configuration template
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Docker configuration
└── docker-compose.yml         # Docker compose setup
```

## ⚡ Fast Start (5 minutes)

### Option 1: Using Python (Recommended)

**Windows:**
```bash
# 1. Navigate to project
cd C:\Users\Aakarshana\Desktop\smart_textpal

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

**macOS/Linux:**
```bash
cd smart_textpal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Option 2: Using Docker (Quickest)

```bash
docker-compose up --build
```

### Option 3: Run Setup Script

```bash
python setup.py
```

Once running, open **http://localhost:5000** in your browser.

## 🎯 How to Use

### 1. **Upload a Document**
- Click the upload area or drag-and-drop a `.txt` or `.pdf` file
- Supported formats: `.txt` (plain text), `.pdf`
- Maximum file size: 50MB

### 2. **Read Aloud**
- Click 🔊 **Read Aloud** to hear the text
- Click ⏹️ **Stop** to pause
- Uses browser's native text-to-speech

### 3. **Analyze Text**
- 📊 **Analyze Difficulty**: Get Flesch Reading Ease score
  - 90-100: Very Easy
  - 80-89: Easy
  - 70-79: Fairly Easy
  - 60-69: Standard
  - 50-59: Fairly Difficult
  - 30-49: Difficult
  - 0-29: Very Difficult

### 4. **Get Summary**
- 📝 **Summarize**: AI generates concise summary
- Uses BART model for abstractive summarization

### 5. **Extract Keywords**
- 🔑 **Extract Keywords**: Identifies 10 key topics
- Helps focus on important concepts

### 6. **Translate**
- 🌐 **Translate to Tamil**: Converts English ↔ Tamil
- Uses Helsinki-NLP translation models

### 7. **Ask Questions**
- 💬 **Chatbot**: Ask any question about the document
- AI answers based on text content
- Uses DistilBERT for question answering

### 8. **Customize Display**
- **Font Size**: Small → Medium → Large → Extra Large
- **Font Type**: 
  - Default (sans-serif)
  - Dyslexia-friendly (OpenDyslexic)
  - Serif
  - Monospace
- **Dark Mode**: Toggle with 🌙 button

## 🔧 API Reference

All endpoints use JSON and the base URL is `http://localhost:5000/api`

### File Operations
```
POST /api/upload
Body: FormData with 'file' field
Response: { text, filename, word_count, char_count }
```

### Text Analysis
```
POST /api/analyze-difficulty
Body: { "text": "..." }
Response: { score, level, num_sentences, num_words }

POST /api/summarize
Body: { "text": "...", "max_length": 150, "min_length": 50 }
Response: { summary, original_length, summary_length }

POST /api/extract-keywords
Body: { "text": "...", "num_keywords": 10 }
Response: { keywords: [...] }
```

### Translation
```
POST /api/translate
Body: { "text": "...", "target_language": "ta" }
Response: { original_text, translated_text, target_language }

POST /api/detect-language
Body: { "text": "..." }
Response: { language, language_name }
```

### Chatbot
```
POST /api/ask-question
Body: { "question": "..." }
Response: { question, answer, conversation_history }

GET /api/chat-history
Response: { history: [...] }

POST /api/clear-chat
Response: { success, message }
```

### System
```
GET /api/health
Response: { status, message }
```

## 📦 Installation Details

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8+ 
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 5GB (for models)
- **Browser**: Modern (Chrome, Firefox, Edge, Safari)

### Dependencies Installed
1. **Flask** - Web framework
2. **PyPDF2** - PDF extraction
3. **Transformers** - AI models (summarization, Q&A, translation)
4. **PyTorch** - Deep learning framework
5. **Flask-CORS** - Cross-origin requests

### First-Time Setup
⚠️ **Important**: Models download on first use (~2GB). This may take 5-10 minutes. Be patient!

To pre-download:
```bash
python -c "from transformers import pipeline; pipeline('summarization', model='facebook/bart-large-cnn')"
```

## 🧪 Testing

Run the test suite:
```bash
pytest test_textpal.py -v
```

Run with coverage:
```bash
pytest test_textpal.py --cov=utils
```

## 📝 Development

### Install Dev Dependencies
```bash
pip install -r requirements-dev.txt
```

### Code Quality
```bash
# Format code
black .

# Check for issues
flake8 .

# Lint
pylint app.py utils/
```

## 🐛 Troubleshooting

### Issue: Port 5000 already in use
```bash
# Kill the process on Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On macOS/Linux
lsof -i :5000
kill -9 <PID>

# Or change port in app.py:
# app.run(port=5001)
```

### Issue: Models not downloading
```bash
pip install --upgrade transformers torch
python app.py
```

### Issue: PDF extraction fails
- Ensure PDF is not corrupted
- Try a different PDF file
- Check file size (< 50MB)

### Issue: Chatbot not responding
- Load a document first
- Check if text is sufficient (100+ characters)
- Verify internet connection

### Issue: Translation fails
- Check language detection
- Try shorter text snippets
- Ensure both Tamil and English inputs work

## 🚀 Deployment

### Deploy to Heroku
```bash
# Install Heroku CLI
# Create Procfile:
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create textpal-app
git push heroku main
```

### Deploy with Docker
```bash
docker build -t textpal .
docker run -p 5000:5000 textpal
```

### Deploy to Cloud
- **AWS**: Use Elastic Beanstalk or EC2
- **Google Cloud**: Use App Engine or Cloud Run
- **Azure**: Use App Service or Container Instances
- **DigitalOcean**: Use App Platform

See README.md for detailed deployment guide.

## 📚 Key Features Explained

### Flesch Reading Ease Score
Measures text complexity: `206.835 - 1.015(words/sentences) - 84.6(syllables/words)`

### Dyslexia-Friendly Font
OpenDyslexic features:
- Unique letter shapes prevent confusion (b/d)
- Larger fonts and spacing
- Improves readability for dyslexic readers

### BART Summarization
Facebook's BART model for:
- Abstractive (not extractive) summaries
- Preserves meaning
- Better than traditional methods

### DistilBERT Q&A
For accurate answers:
- Finds relevant passages
- Generates responses
- Provides confidence scores

## 🤝 Contributing

We welcome contributions! See CONTRIBUTING.md for:
- Code style guidelines
- Testing requirements
- Pull request process
- Feature ideas

## 📄 License

MIT License - Feel free to use and modify!

## 🎓 Learning Resources

- **Flask**: https://flask.palletsprojects.com/
- **Transformers**: https://huggingface.co/transformers/
- **NLP**: https://www.coursera.org/learn/natural-language-processing-specialization
- **Accessibility**: https://www.w3.org/WAI/

## 💡 Next Steps

1. ✅ Explore all features
2. ✅ Try uploading different documents
3. ✅ Customize fonts and colors
4. ✅ Test the chatbot
5. ✅ Review the code
6. ✅ Deploy to production
7. ✅ Contribute improvements

## 📞 Support

- 📖 Read README.md for full documentation
- 🔍 Check test_textpal.py for code examples
- 🐛 Report issues with details
- 💬 Discussion forum in GitHub Issues

---

## 🎉 You're All Set!

Your TextPal application is ready to transform reading accessibility. 

**Start with**: http://localhost:5000

Enjoy! 📚✨

---

*Built with ❤️ for better reading comprehension and accessibility*
