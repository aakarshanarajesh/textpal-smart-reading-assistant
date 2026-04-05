/**
 * Smart Reading Assistant (TextPal) - Main JavaScript
 * Handles all frontend functionality and API interactions
 */

// ============================================
// Global Variables
// ============================================

let currentText = '';
let isReading = false;
let speechSynthesis = window.speechSynthesis;
const API_BASE = 'http://localhost:5000/api';

// ============================================
// DOM Elements
// ============================================

const fileUploadArea = document.getElementById('file-upload-area');
const fileInput = document.getElementById('file-input');
const fileInfo = document.getElementById('file-info');
const textDisplay = document.getElementById('text-display');
const speakBtn = document.getElementById('speak-btn');
const stopSpeakBtn = document.getElementById('stop-speak-btn');
const summarizeBtn = document.getElementById('summarize-btn');
const analyzeBtn = document.getElementById('analyze-btn');
const keywordsBtn = document.getElementById('keywords-btn');
const translateBtn = document.getElementById('translate-btn');
const askBtn = document.getElementById('ask-btn');
const clearChatBtn = document.getElementById('clear-chat-btn');
const questionInput = document.getElementById('question-input');
const chatOutput = document.getElementById('chat-output');
const loadingSpinner = document.getElementById('loading-spinner');
const toastContainer = document.getElementById('toast-container');
const fontSizeSelect = document.getElementById('font-size-select');
const fontFamilySelect = document.getElementById('font-family-select');
const darkModeToggle = document.getElementById('dark-mode-toggle');
const analysisPanel = document.getElementById('analysis-panel');

// ============================================
// Event Listeners - File Upload
// ============================================

// Click to upload
fileUploadArea.addEventListener('click', () => {
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        uploadFile(file);
    }
});

// Drag and drop
fileUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadArea.style.borderColor = '#2ecc71';
    fileUploadArea.style.backgroundColor = 'rgba(46, 204, 113, 0.05)';
});

fileUploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    fileUploadArea.style.borderColor = '#3498db';
    fileUploadArea.style.backgroundColor = 'rgba(52, 152, 219, 0.05)';
});

fileUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadArea.style.borderColor = '#3498db';
    fileUploadArea.style.backgroundColor = 'rgba(52, 152, 219, 0.05)';

    const file = e.dataTransfer.files[0];
    if (file) {
        uploadFile(file);
    }
});

// ============================================
// Event Listeners - Buttons
// ============================================

speakBtn.addEventListener('click', readAloud);
stopSpeakBtn.addEventListener('click', stopReading);
summarizeBtn.addEventListener('click', summarizeText);
analyzeBtn.addEventListener('click', analyzeDifficulty);
keywordsBtn.addEventListener('click', extractKeywords);
translateBtn.addEventListener('click', translateText);
askBtn.addEventListener('click', askQuestion);
clearChatBtn.addEventListener('click', clearChat);

// Text input enter key
questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        askQuestion();
    }
});

// Font customization
fontSizeSelect.addEventListener('change', (e) => {
    const size = e.target.value;
    textDisplay.className = 'text-display ' + size;
    localStorage.setItem('textSize', size);
});

fontFamilySelect.addEventListener('change', (e) => {
    const family = e.target.value;
    textDisplay.className = 'text-display ' + family;
    localStorage.setItem('fontFamily', family);
});

// Dark mode toggle
darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
    darkModeToggle.textContent = isDarkMode ? '☀️' : '🌙';
});

// ============================================
// File Upload Function
// ============================================

async function uploadFile(file) {
    // Validate file type
    const validTypes = ['text/plain', 'application/pdf'];
    if (!validTypes.includes(file.type)) {
        showToast('Only .txt and .pdf files are supported', 'error');
        return;
    }

    // Validate file size (50MB max)
    if (file.size > 50 * 1024 * 1024) {
        showToast('File size must be less than 50MB', 'error');
        return;
    }

    showLoading(true);

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }

        // Store text
        currentText = data.text;

        // Update UI
        textDisplay.textContent = currentText;
        textDisplay.classList.remove('placeholder');

        // Update file info
        document.getElementById('current-filename').textContent = data.filename;
        document.getElementById('word-count').textContent = data.word_count;
        document.getElementById('char-count').textContent = data.char_count;
        fileInfo.style.display = 'block';

        // Enable buttons
        enableButtons(true);

        showToast(`File uploaded successfully! ${data.word_count} words loaded.`, 'success');
    } catch (error) {
        console.error('Upload error:', error);
        showToast('Error uploading file: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// ============================================
// Text-to-Speech Function
// ============================================

function readAloud() {
    if (!currentText) {
        showToast('No text to read', 'error');
        return;
    }

    if (isReading) {
        return;
    }

    isReading = true;
    speakBtn.style.opacity = '0.5';
    stopSpeakBtn.disabled = false;

    const utterance = new SpeechSynthesisUtterance(currentText);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    utterance.onend = () => {
        isReading = false;
        speakBtn.style.opacity = '1';
        stopSpeakBtn.disabled = true;
        showToast('Reading completed', 'info');
    };

    utterance.onerror = (event) => {
        isReading = false;
        speakBtn.style.opacity = '1';
        showToast('Error during text reading: ' + event.error, 'error');
    };

    speechSynthesis.speak(utterance);
    showToast('Starting to read...', 'info');
}

function stopReading() {
    speechSynthesis.cancel();
    isReading = false;
    speakBtn.style.opacity = '1';
    stopSpeakBtn.disabled = true;
    showToast('Reading stopped', 'info');
}

// ============================================
// Text Analysis Functions
// ============================================

async function summarizeText() {
    if (!currentText) {
        showToast('No text to summarize', 'error');
        return;
    }

    showLoading(true);
    analysisPanel.style.display = 'block';

    try {
        const response = await fetch(`${API_BASE}/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: currentText,
                max_length: 150,
                min_length: 50
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Summarization failed');
        }

        // Display summary
        document.getElementById('summary-text').textContent = data.summary;
        document.getElementById('summary-result').style.display = 'block';

        showToast('Summary generated successfully!', 'success');
    } catch (error) {
        console.error('Summarization error:', error);
        showToast('Error summarizing text: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function analyzeDifficulty() {
    if (!currentText) {
        showToast('No text to analyze', 'error');
        return;
    }

    showLoading(true);
    analysisPanel.style.display = 'block';

    try {
        const response = await fetch(`${API_BASE}/analyze-difficulty`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: currentText
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        // Display difficulty analysis
        document.getElementById('difficulty-score').textContent = data.score;
        document.getElementById('difficulty-level').textContent = data.level;
        document.getElementById('sentence-count').textContent = data.num_sentences;
        document.getElementById('difficulty-result').style.display = 'block';

        showToast('Difficulty analysis completed!', 'success');
    } catch (error) {
        console.error('Difficulty analysis error:', error);
        showToast('Error analyzing text: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function extractKeywords() {
    if (!currentText) {
        showToast('No text to extract keywords from', 'error');
        return;
    }

    showLoading(true);
    analysisPanel.style.display = 'block';

    try {
        const response = await fetch(`${API_BASE}/extract-keywords`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: currentText,
                num_keywords: 10
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Keyword extraction failed');
        }

        // Display keywords
        const keywordsList = document.getElementById('keywords-list');
        keywordsList.innerHTML = data.keywords
            .map(keyword => `<span class="keyword-tag">${keyword}</span>`)
            .join('');
        document.getElementById('keywords-result').style.display = 'block';

        showToast('Keywords extracted successfully!', 'success');
    } catch (error) {
        console.error('Keyword extraction error:', error);
        showToast('Error extracting keywords: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function translateText() {
    if (!currentText) {
        showToast('No text to translate', 'error');
        return;
    }

    showLoading(true);
    analysisPanel.style.display = 'block';

    try {
        const response = await fetch(`${API_BASE}/translate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: currentText,
                target_language: 'ta'  // Translate to Tamil
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Translation failed');
        }

        // Display translation
        document.getElementById('translation-original').textContent = data.original_text;
        document.getElementById('translation-tamil').textContent = data.translated_text;
        document.getElementById('translation-result').style.display = 'block';

        showToast('Translation completed successfully!', 'success');
    } catch (error) {
        console.error('Translation error:', error);
        showToast('Error translating text: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// ============================================
// Chatbot Functions
// ============================================

async function askQuestion() {
    const question = questionInput.value.trim();

    if (!question) {
        showToast('Please enter a question', 'error');
        return;
    }

    if (!currentText) {
        showToast('No document loaded', 'error');
        return;
    }

    // Add user message to chat
    addChatMessage(question, 'user');
    questionInput.value = '';

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE}/ask-question`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Question processing failed');
        }

        // Add bot response to chat
        addChatMessage(data.answer, 'bot');
    } catch (error) {
        console.error('Question error:', error);
        addChatMessage('Sorry, I could not process your question: ' + error.message, 'bot');
    } finally {
        showLoading(false);
    }
}

function addChatMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.className = `chat-message ${sender}`;
    messageElement.textContent = message;
    chatOutput.appendChild(messageElement);
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

async function clearChat() {
    try {
        const response = await fetch(`${API_BASE}/clear-chat`, {
            method: 'POST'
        });

        if (response.ok) {
            chatOutput.innerHTML = '';
            showToast('Chat history cleared', 'success');
        }
    } catch (error) {
        console.error('Clear chat error:', error);
        showToast('Error clearing chat', 'error');
    }
}

// ============================================
// UI Helper Functions
// ============================================

function enableButtons(enable) {
    speakBtn.disabled = !enable;
    summarizeBtn.disabled = !enable;
    analyzeBtn.disabled = !enable;
    keywordsBtn.disabled = !enable;
    translateBtn.disabled = !enable;
    questionInput.disabled = !enable;
    askBtn.disabled = !enable;
    clearChatBtn.disabled = !enable;
}

function showLoading(show) {
    loadingSpinner.style.display = show ? 'flex' : 'none';
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    toastContainer.appendChild(toast);

    // Auto remove after 4 seconds
    setTimeout(() => {
        toast.remove();
    }, 4000);
}

// ============================================
// Local Storage - Load Preferences
// ============================================

function loadPreferences() {
    // Load dark mode
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        darkModeToggle.textContent = '☀️';
    }

    // Load text size
    const textSize = localStorage.getItem('textSize') || 'medium';
    fontSizeSelect.value = textSize;
    textDisplay.classList.add(textSize);

    // Load font family
    const fontFamily = localStorage.getItem('fontFamily') || 'default';
    fontFamilySelect.value = fontFamily;
    if (fontFamily !== 'default') {
        textDisplay.classList.add(fontFamily);
    }
}

// ============================================
// Initialization
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('TextPal loaded successfully!');
    loadPreferences();
    enableButtons(false);

    // Check API health
    fetch(`${API_BASE}/health`)
        .then(response => response.json())
        .then(data => console.log('API Status:', data.status))
        .catch(error => console.error('API connection error:', error));
});

// ============================================
// Error Handling
// ============================================

window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});
