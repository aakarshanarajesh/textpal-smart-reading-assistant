"""
Chatbot Module
Simple chatbot for handling user queries
"""

import re
import os
from collections import Counter

qa_pipeline = None
qa_pipeline_loaded = False


def get_qa_pipeline():
    """Load the QA model only when a question is asked."""
    global qa_pipeline, qa_pipeline_loaded

    if os.getenv('ENABLE_ML_QA', '').lower() not in {'1', 'true', 'yes'}:
        return None

    if qa_pipeline_loaded:
        return qa_pipeline

    qa_pipeline_loaded = True
    try:
        from transformers import pipeline
        qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", device=-1)
    except Exception:
        qa_pipeline = None

    return qa_pipeline


class SimpleChatbot:
    """Simple chatbot that answers questions about the uploaded text"""
    
    def __init__(self):
        self.context = ""
        self.conversation_history = []
    
    def set_context(self, text):
        """
        Set the context (document) for the chatbot
        
        Args:
            text (str): The document text to use as context
        """
        # Limit context size to avoid model overload
        if len(text) > 3000:
            self.context = text[:3000]
        else:
            self.context = text
    
    def ask_question(self, question):
        """
        Ask a question about the context
        
        Args:
            question (str): Question to ask
            
        Returns:
            str: Answer to the question
        """
        if not self.context:
            return "Please upload a document first."
        
        model = get_qa_pipeline()

        if not model:
            answer = self.simple_answer(question)
            self.conversation_history.append({
                'question': question,
                'answer': answer,
                'confidence': None
            })
            return answer
        
        try:
            # Use QA pipeline to answer question
            result = model(question=question, context=self.context)
            answer = result['answer']
            confidence = result['score']
            
            # Store in conversation history
            self.conversation_history.append({
                'question': question,
                'answer': answer,
                'confidence': confidence
            })
            
            return answer
        except Exception as e:
            return self.simple_answer(question)

    def simple_answer(self, question):
        """Find the most relevant sentence when the ML QA model is unavailable."""
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', self.context) if s.strip()]
        if not sentences:
            return "I could not find readable text in the document."

        question_words = {
            word for word in re.findall(r'\b[a-zA-Z]{3,}\b', question.lower())
            if word not in {'what', 'when', 'where', 'which', 'about', 'does', 'this', 'that', 'with', 'from', 'have', 'name'}
        }

        if 'name' in question.lower():
            name_match = re.search(r'\b(?:name is|named|I am|my name is)\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2})', self.context)
            if name_match:
                return name_match.group(1)

        if not question_words:
            question_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', question.lower()))

        scored_sentences = []
        for sentence in sentences:
            sentence_words = Counter(re.findall(r'\b[a-zA-Z]{3,}\b', sentence.lower()))
            score = sum(sentence_words[word] for word in question_words)
            if score:
                scored_sentences.append((score, sentence))

        if scored_sentences:
            scored_sentences.sort(key=lambda item: item[0], reverse=True)
            return scored_sentences[0][1]

        return "I could not find a direct answer in the document. Try asking with words that appear in the text."
    
    def get_conversation_history(self):
        """
        Get conversation history
        
        Returns:
            list: List of question-answer pairs
        """
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
