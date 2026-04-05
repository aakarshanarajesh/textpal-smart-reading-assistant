# Smart Reading Assistant (TextPal) 📚

A comprehensive web-based application designed to improve reading accessibility and comprehension through AI-powered features.

## Features

### Core Features
- **📁 File Upload**: Support for `.txt` and `.pdf` files
- **📖 Clean Text Display**: Beautiful, readable text presentation
- **🔊 Text-to-Speech**: Read content aloud with stop functionality
- **📝 Summarization**: Auto-generate summaries using AI
- **📊 Difficulty Analysis**: Calculate Flesch Reading Ease score
- **🎨 Font Customization**: 
  - Multiple font families (including dyslexia-friendly OpenDyslexic)
  - Adjustable font sizes (Small, Medium, Large, Extra Large)
  - Dark mode support
- **💬 AI Chatbot**: Ask questions about the uploaded text
- **🌐 Multi-language Translation**: English ↔ Tamil translation
- **🔑 Keyword Extraction**: Identify important topics
- **✨ Responsive UI**: Works on desktop, tablet, and mobile

## Project Structure

```
smart_textpal/
├── app.py                  # Flask backend application
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css      # Complete styling
│   └── js/
│       └── main.js        # Frontend functionality
├── utils/
│   ├── text_extraction.py # PDF/TXT extraction
│   ├── text_processing.py # Summarization & difficulty analysis
│   ├── translation.py     # Language translation
│   └── chatbot.py         # QA chatbot
└── uploads/               # Uploaded files storage
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Download Project
```bash
git clone <repository-url>
cd smart_textpal
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download Required Models (Optional)
The app will download transformer models on first use. This may take several minutes:
```bash
python -c "from transformers import pipeline; pipeline('summarization', model='facebook/bart-large-cnn')"
python -c "from transformers import pipeline; pipeline('question-answering', model='distilbert-base-cased-distilled-squad')"
```

### Step 5: Run the Application
```bash
python app.py
```

The application will start at `http://localhost:5000`

## Usage Guide

### 1. Upload a Document
- Click the upload area or drag & drop a `.txt` or `.pdf` file
- The text will be extracted and displayed in the main area

### 2. Read Aloud
- Click **"Read Aloud"** button to have the text read by the browser
- Use **"Stop"** button to pause the reading
- Adjust playback rate using browser speech controls

### 3. Summarize Content
- Click **"Summarize"** to generate an AI-powered summary
- Summary appears in the analysis panel

### 4. Analyze Difficulty
- Click **"Analyze Difficulty"** to get Flesch Reading Ease score
- Score ranges 0-100:
  - 90-100: Very Easy
  - 80-89: Easy
  - 70-79: Fairly Easy
  - 60-69: Standard
  - 50-59: Fairly Difficult
  - 30-49: Difficult
  - 0-29: Very Difficult

### 5. Extract Keywords
- Click **"Extract Keywords"** to identify important topics
- Keywords are displayed as tags

### 6. Translate to Tamil
- Click **"Translate to Tamil"** for English→Tamil translation
- Original and translated text displayed side-by-side

### 7. Ask Questions (Chatbot)
- Type questions about the document in the chatbox
- AI will answer based on the document content
- Chat history is maintained during session

### 8. Customize Display
- **Font Size**: Adjust text size for readability
- **Font Type**: Choose dyslexia-friendly or other fonts
- **Dark Mode**: Toggle dark/light theme

## API Endpoints

### File Upload
```
POST /api/upload
- File: binary (PDF or TXT)
- Returns: Extracted text, word count, char count
```

### Text Analysis
```
POST /api/analyze-difficulty
- Body: { "text": "..." }
- Returns: Score, level, word/sentence count

POST /api/summarize
- Body: { "text": "...", "max_length": 150, "min_length": 50 }
- Returns: Summary text

POST /api/extract-keywords
- Body: { "text": "...", "num_keywords": 10 }
- Returns: List of keywords
```

### Translation
```
POST /api/translate
- Body: { "text": "...", "target_language": "ta" }
- Returns: Original and translated text

POST /api/detect-language
- Body: { "text": "..." }
- Returns: Detected language (en/ta)
```

### Chatbot
```
POST /api/ask-question
- Body: { "question": "..." }
- Returns: Answer, conversation history

GET /api/chat-history
- Returns: Conversation history

POST /api/clear-chat
- Returns: Success confirmation
```

## Technology Stack

### Backend
- **Flask**: Web framework
- **PyPDF2**: PDF text extraction
- **Transformers**: Hugging Face models for:
  - Text summarization (BART)
  - Question answering (DistilBERT)
  - Translation (Helsinki-NLP OPUS-MT)
- **PyTorch**: Deep learning backend

### Frontend
- **HTML5**: Page structure
- **CSS3**: Responsive styling
- **Vanilla JavaScript**: Interactivity
- **Web Speech API**: Text-to-speech

## Features Explained

### Flesch Reading Ease Score
Measures text complexity based on:
- Sentence length
- Word length
- Syllable count

Formula: `206.835 - 1.015(words/sentences) - 84.6(syllables/words)`

### Dyslexia-Friendly Font
OpenDyslexic font features:
- Unique character shapes for clarity
- Increased letter spacing
- Larger font heights
- Recommended by dyslexia communities

### AI Summarization
Uses Facebook's BART model to:
- Generate abstractive summaries
- Preserve key information
- Adapt to requested length

### Question Answering
Uses DistilBERT model to:
- Find relevant passages
- Generate accurate answers
- Provide confidence scores

## Performance Tips

1. **First Run**: Models will download (~2GB). Be patient!
2. **Large Files**: Text summarization works best with 500-2000 words
3. **Translation**: Works for English↔Tamil (other languages can be added)
4. **Chatbot**: Best results with a 500-3000 character context

## Troubleshooting

### Issue: Models not downloading
**Solution**: 
```bash
pip install --upgrade transformers torch
python app.py
```

### Issue: API connection errors
**Solution**: Make sure Flask is running on port 5000 and CORS is enabled

### Issue: TTS not working
**Solution**: 
- Use a modern browser (Chrome, Edge, Firefox)
- Check if speech synthesis is available in your region

### Issue: Large PDFs fail
**Solution**: 
- Try splitting the PDF into smaller files
- Maximum file size is 50MB

## Future Enhancements

- [ ] Support for more file formats (DOCX, PPT)
- [ ] Additional languages for translation
- [ ] Bookmark and favorites system
- [ ] Progress tracking and reading statistics
- [ ] Accessibility features (ARIA labels, keyboard navigation)
- [ ] Collaborative reading sessions
- [ ] Mobile app version

## System Requirements

### Minimum
- 4GB RAM
- 5GB disk space (for models)
- Python 3.8+

### Recommended
- 8GB RAM
- GPU support (for faster processing)
- Modern web browser

## License

This project is open-source and available under the MIT License.

## Support & Contact

For issues, suggestions, or contributions, please open an issue in the repository.

## Acknowledgments

- **Hugging Face**: For pre-trained models
- **OpenDyslexic**: For dyslexia-friendly font
- **Flask Community**: For excellent documentation
- **Open Source Contributors**: For various libraries

---

**Happy Reading! 📚✨**

Built with ❤️ for better accessibility and comprehension.
