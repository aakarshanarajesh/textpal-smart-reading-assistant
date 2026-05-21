"""
Chatbot Module
Simple chatbot for handling user queries
"""


qa_pipeline = None
qa_pipeline_loaded = False


def get_qa_pipeline():
    """Load the QA model only when a question is asked."""
    global qa_pipeline, qa_pipeline_loaded

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
            return "QA service unavailable. Please check dependencies."
        
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
            return f"Error processing question: {str(e)}"
    
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
