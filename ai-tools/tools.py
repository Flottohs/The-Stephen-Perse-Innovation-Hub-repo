import transformers
import torch 

class SemanticsAnalyzer:
    """Analyzes the semantic meaning and emotions of text"""
    
    def __init__(self):
        self.model = None
    
    def init_model(self):
        print("Loading sentiment analysis model...")
        self.model = transformers.pipeline('sentiment-analysis', model='SamLowe/roberta-base-go_emotions', top_k=None)
        print("✓ Sentiment model ready!")
    
    def process_query(self, text):
        output = self.model(text)[0]
        top_k = 5 
        
        results = ""
        
        for k in range(top_k):
            results += f"{output[k]['label']}, confidence: {round(output[k]['score'], 4)}\n"
            
        return results
        
class ImageClassifier:
    """Classifies what objects appear in an image"""
    
    def __init__(self):
        self.model = None
    
    def init_model(self):
        print("Loading image classification model...")
        self.model = transformers.pipeline('image-classification', 
                            model='google/vit-base-patch16-224')
        print("✓ Image classifier ready!")
    
    def process_query(self, image):
        results = self.model(image)
        
        label = results[0]['label']
        confidence = round(results[0]['score'] * 100, 3)
        secondary_label = results[1]['label']
        secondary_confidence = round(results[1]['score'] * 100, 3)
        
        results = f"I am {confidence}% sure it is {label}, but it might also be {secondary_label}, which I am {secondary_confidence}% sure about"
        
        return results
        
class TextSummarizer:
    """Summarizes long text into shorter versions"""
    
    def __init__(self):
        self.model = None
    
    def init_model(self):
        print("Loading summarization model...")
        self.model = transformers.pipeline('summarization', 
                            model='facebook/bart-large-cnn')
        print("✓ Summarizer ready!")
    
    def process_query(self, text):
        # Generate summary
        max_length = 200
        summary_result = self.model(text, 
                                   max_length=80,
                                    temperature=0.7,
                                    top_k=50,
                                    top_p=0.9,
                                    repetition_penalty=1.5,
                                    no_repeat_ngram_size=2,
                                    do_sample=True,
                                    pad_token_id=50256,
                                    eos_token_id=50256)
        summary = summary_result[0]['summary_text']
        
        original_words = len(text.split())
        summary_words = len(summary.split())
        reduction = round((1 - summary_words / original_words) * 100)
        
        results = f'''Here you go!
        {summary}
        Original text: {original_words} words, Summary: {summary_words} words. That's a {reduction}% reduction!'''
        
        return results

class HaikuWriter:
    def __init__(self):
        self.generator = None

    def init_model(self):
        self.generator = transformers.pipeline(
            'text-generation',
            model='HuggingFaceTB/SmolLM2-135M-Instruct',
            device=-1 # CPU
        )

    def process_query(self, topic):
        # We use a chat-style template which this model understands perfectly
        messages = [
            {"role": "user",
             "content": f"Write a short 3-line haiku about {topic}. No extra text."}
        ]

        # This model handles the prompt formatting for us
        result = self.generator(
            messages,
            max_new_tokens=50,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95
        )

        # Extract only the assistant's response
        haiku = result[0]['generated_text'][-1]['content']

        return f"Here's a haiku about {topic}:\n{haiku}"
    
class RPGQuestGenerator:
    """Generates a video game quest based on a location or theme"""

    def __init__(self):
        self.generator = None

    def init_model(self):
        self.generator = transformers.pipeline(
            'text-generation',
            model='HuggingFaceTB/SmolLM2-135M-Instruct',
            device=-1 # CPU
        )

    def process_query(self, setting):
        messages = [
            {"role": "user",
             "content": f"You are a Game Master. Write a short, single-sentence quest objective for a player (3rd-person grammar) in: {setting}."}
        ]

        result = self.generator(
            messages,
            max_new_tokens=60,
            do_sample=True,
            temperature=0.8, # Slightly higher for creativity
            top_k=50,
            top_p=0.95
        )

        # Extract only the assistant's response
        quest = result[0]['generated_text'][-1]['content']

        return f"⚔️ New Quest in [{setting}]:\n{quest}"
    
class WhyExplainer:
    """Explains 'why' something works the way it does"""

    def __init__(self):
        self.generator = None

    def init_model(self):
        self.generator = transformers.pipeline(
            'text-generation',
            model='HuggingFaceTB/SmolLM2-135M-Instruct',
            device=-1 # CPU
        )

    def process_query(self, question):
        messages = [
            {"role": "user",
             "content": f"Explain clearly and concisely: {question}"}
        ]

        result = self.generator(
            messages,
            max_new_tokens=200, # Increased for explanations
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95
        )

        answer = result[0]['generated_text'][-1]['content']
        return f"Here is an answer to your question: \n{answer}"