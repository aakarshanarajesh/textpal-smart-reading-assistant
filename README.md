# Smart Reading Assistant (TextPal)

Smart Reading Assistant, also called TextPal, is a Flask web application for reading support, document understanding, and accessibility. Users can upload PDF or TXT files, view extracted text, listen with browser text-to-speech, generate summaries, analyze reading difficulty, extract keywords, and ask questions about the uploaded document.

## Features

- Upload and extract text from PDF and TXT files.
- Display document text in a clean, responsive reading interface.
- Read content aloud with browser text-to-speech controls.
- Generate AI-powered summaries when `OPENAI_API_KEY` is configured.
- Fall back to lightweight NLP extractive summarization when AI is unavailable.
- Analyze readability with the Flesch Reading Ease score.
- Extract important keywords from uploaded text.
- Ask document-based questions through a simple QA chatbot.
- Customize font family, font size, and dark mode.
- Use the app on desktop, tablet, and mobile screens.

## Tech Stack

- Backend: Flask, Flask-CORS, Werkzeug
- AI and NLP: OpenAI-compatible chat completions, lightweight NLP fallbacks
- File processing: PyPDF2
- Frontend: HTML, CSS, JavaScript
- Browser feature: Web Speech API
- Deployment support: Docker, Render, Vercel configuration

## Project Structure

```text
smart_textpal/
|-- app.py
|-- config.py
|-- requirements.txt
|-- requirements-dev.txt
|-- Procfile
|-- runtime.txt
|-- vercel.json
|-- Dockerfile
|-- docker-compose.yml
|-- templates/
|   `-- index.html
|-- static/
|   |-- css/
|   |   `-- style.css
|   `-- js/
|       `-- main.js
|-- utils/
|   |-- chatbot.py
|   |-- text_extraction.py
|   |-- text_processing.py
|   `-- translation.py
|-- uploads/
|   `-- .gitkeep
|-- check_system.py
`-- test_textpal.py
```

## Local Setup

### AI/NLP features

TextPal uses AI-powered summarization and document Q&A when `OPENAI_API_KEY` is configured on the backend. Without a key, it falls back to lightweight NLP extractive summarization and document sentence matching so uploads and summaries still work.

Render environment variables:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Optional local transformer mode:

```env
ENABLE_LOCAL_TRANSFORMERS=true
ENABLE_ML_QA=true
```

### Prerequisites

- Python 3.8 or newer
- pip
- Git

### Install

```bash
git clone <repository-url>
cd smart_textpal
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# macOS or Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

## Optional Model Warmup

The first AI request may download large model files. To warm up the main models in advance, run:

```bash
python -c "from transformers import pipeline; pipeline('summarization', model='facebook/bart-large-cnn')"
python -c "from transformers import pipeline; pipeline('question-answering', model='distilbert-base-cased-distilled-squad')"
```

## Environment Variables

Copy `.env.example` to `.env` for local configuration:

```bash
cp .env.example .env
```

Important values:

- `FLASK_ENV`: Use `development` locally and `production` in production.
- `FLASK_DEBUG`: Use `True` locally and `False` in production.
- `FLASK_HOST`: Defaults to `0.0.0.0`.
- `FLASK_PORT`: Defaults to `5000`.
- `MAX_FILE_SIZE`: Maximum upload size in bytes.

## API Endpoints

```text
GET  /api/health
POST /api/upload
POST /api/analyze-difficulty
POST /api/summarize
POST /api/extract-keywords
POST /api/translate
POST /api/detect-language
POST /api/ask-question
GET  /api/chat-history
POST /api/clear-chat
```

## Deployment

### Recommended: Render

Render is recommended for this project because the backend uses PyTorch and Hugging Face models. These dependencies are large and need more runtime flexibility than typical serverless deployments provide.

Render setup:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Python version: defined in `runtime.txt`
- Environment: set production values such as `FLASK_ENV=production` and `FLASK_DEBUG=False`

The included `Procfile` is ready for Render-style deployment.

### Vercel

This repository includes a `vercel.json` file so Vercel can recognize the Flask app. However, deploying the full AI backend on Vercel is likely to fail or perform poorly because PyTorch and Transformer model downloads are large, cold starts are slow, and serverless functions have size and execution limits.

Use Vercel only if:

- You deploy a lightweight version of the Flask app without heavy local models, or
- You split the project so Vercel hosts the frontend and Render hosts the Flask API.

For the current full-stack Flask app, Render is required for a reliable deployment.

## Docker

Build and run with Docker:

```bash
docker build -t smart-textpal .
docker run -p 5000:5000 smart-textpal
```

Or use Docker Compose:

```bash
docker-compose up --build
```

## Usage

1. Upload a `.txt` or `.pdf` document.
2. Review the extracted text in the reader.
3. Use summary, readability, keyword, translation, or chatbot tools.
4. Adjust font size, font family, and dark mode for better reading comfort.

## Troubleshooting

### Models are slow on first use

The app downloads model files the first time AI features run. This can take several minutes depending on network speed.

### Translation or chatbot is unavailable

Check that `transformers`, `torch`, and the required model dependencies installed correctly:

```bash
pip install --upgrade -r requirements.txt
```

### Large PDFs fail

Try a smaller file or split the document. The default maximum upload size is 50 MB.

### Vercel deployment fails

Use Render for the backend, or move the AI features to a hosted model API. The current local-model setup is too heavy for a typical Vercel serverless deployment.

## Testing

Run the test suite:

```bash
pytest
```

Run the system check:

```bash
python check_system.py
```

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Hugging Face for pre-trained NLP models.
- OpenDyslexic for dyslexia-friendly font support.
- Flask and the Python open-source community.
