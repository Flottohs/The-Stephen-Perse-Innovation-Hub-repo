"""
AI Tools Module
Each tool follows the same protocol:
1. init_model() - Load your AI model (called once at startup)
2. process_query(input) - Process the input and return results

Students: Pick one tool and implement the two functions!
"""

# ============================================================================
# TOOL 1: Semantics Analyzer
# ============================================================================
class SemanticsAnalyzer:
    """Analyzes the semantic meaning and sentiment of text"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
    
    def init_model(self):
        """
        TODO: Load your model here!
        Example: from transformers import pipeline
                 self.model = pipeline('sentiment-analysis')
        """
        # STUDENT IMPLEMENTATION HERE
        print("⚠️  SemanticsAnalyzer: Model not implemented yet!")
        pass
    
    def process_query(self, text):
        """
        TODO: Analyze the text and return semantic information
        Input: text (string)
        Output: dictionary with your analysis
        Example: {'sentiment': 'positive', 'score': 0.95}
        """
        # STUDENT IMPLEMENTATION HERE
        return {
            'sentiment': 'neutral',
            'score': 0.5,
            'message': 'Not implemented yet! Add your code to analyze text.'
        }


# ============================================================================
# TOOL 2: Image Classifier
# ============================================================================
class ImageClassifier:
    """Classifies what objects appear in an image"""
    
    def __init__(self):
        self.model = None
        self.processor = None
    
    def init_model(self):
        """
        TODO: Load your image classification model
        Example: from transformers import pipeline
                 self.model = pipeline('image-classification')
        """
        # STUDENT IMPLEMENTATION HERE
        print("⚠️  ImageClassifier: Model not implemented yet!")
        pass
    
    def process_query(self, image):
        """
        TODO: Classify what's in the image
        Input: image (PIL Image object)
        Output: dictionary with classifications
        Example: {'top_class': 'cat', 'confidence': 0.89, 'all_classes': [...]}
        """
        # STUDENT IMPLEMENTATION HERE
        return {
            'top_class': 'unknown',
            'confidence': 0.0,
            'message': 'Not implemented yet! Add your code to classify images.'
        }


# ============================================================================
# TOOL 3: Text Summarizer
# ============================================================================
class TextSummarizer:
    """Summarizes long text into shorter versions"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
    
    def init_model(self):
        """
        TODO: Load your summarization model
        Example: from transformers import pipeline
                 self.model = pipeline('summarization')
        """
        # STUDENT IMPLEMENTATION HERE
        print("⚠️  TextSummarizer: Model not implemented yet!")
        pass
    
    def process_query(self, text):
        """
        TODO: Summarize the input text
        Input: text (string)
        Output: dictionary with summary
        Example: {'summary': 'Short version of the text...', 'reduction': '75%'}
        """
        # STUDENT IMPLEMENTATION HERE
        return {
            'summary': text[:50] + '...',
            'reduction': '0%',
            'message': 'Not implemented yet! Add your code to summarize text.'
        }


# ============================================================================
# TOOL 4: Joke Generator
# ============================================================================
class JokeGenerator:
    """Generates jokes based on a topic"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
    
    def init_model(self):
        """
        TODO: Load your text generation model
        Example: from transformers import pipeline
                 self.model = pipeline('text-generation', model='gpt2')
        """
        # STUDENT IMPLEMENTATION HERE
        print("⚠️  JokeGenerator: Model not implemented yet!")
        pass
    
    def process_query(self, topic):
        """
        TODO: Generate a joke about the topic
        Input: topic (string)
        Output: dictionary with joke
        Example: {'joke': 'Why did the...', 'topic': topic}
        """
        # STUDENT IMPLEMENTATION HERE
        return {
            'joke': f"I would tell you a joke about {topic}, but I haven't been implemented yet!",
            'topic': topic,
            'message': 'Not implemented yet! Add your code to generate jokes.'
        }


# ============================================================================
# TOOL 5: Haiku Writer
# ============================================================================
class HaikuWriter:
    """Writes haikus about any topic"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
    
    def init_model(self):
        """
        TODO: Load your text generation model
        Example: from transformers import pipeline
                 self.model = pipeline('text-generation')
        """
        # STUDENT IMPLEMENTATION HERE
        print("⚠️  HaikuWriter: Model not implemented yet!")
        pass
    
    def process_query(self, topic):
        """
        TODO: Generate a haiku about the topic
        Input: topic (string)
        Output: dictionary with haiku
        Example: {'haiku': 'Line 1\nLine 2\nLine 3', 'topic': topic}
        """
        # STUDENT IMPLEMENTATION HERE
        return {
            'haiku': 'Code not yet written\nStudents will implement me\nHaiku awaits you',
            'topic': topic,
            'message': 'Not implemented yet! Add your code to write haikus.'
        }


# ============================================================================
# TOOL 6: Why Explainer
# ============================================================================
class WhyExplainer:
    """Explains 'why' something works the way it does"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
    
    def init_model(self):
        """
        TODO: Load your question-answering or text generation model
        Example: from transformers import pipeline
                 self.model = pipeline('text-generation')
        """
        # STUDENT IMPLEMENTATION HERE
        print("⚠️  WhyExplainer: Model not implemented yet!")
        pass
    
    def process_query(self, question):
        """
        TODO: Explain why something works
        Input: question (string) - should start with "Why..."
        Output: dictionary with explanation
        Example: {'explanation': 'This happens because...', 'question': question}
        """
        # STUDENT IMPLEMENTATION HERE
        return {
            'explanation': 'I would explain this, but my code needs to be implemented first!',
            'question': question,
            'message': 'Not implemented yet! Add your code to explain things.'
        }
