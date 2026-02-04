
class SemanticsAnalyzer:
    """Analyzes the semantic meaning and emotions of text"""
    
    def __init__(self):
        self.model = None
    
    def init_model(self):
        from transformers import pipeline
        print("Loading sentiment analysis model...")
        self.model = pipeline('sentiment-analysis', model='SamLowe/roberta-base-go_emotions', top_k=None)
        print("✓ Sentiment model ready!")
    
    def process_query(self, text):
        output = self.model(text)[0]
        top_k = 5 
        
        results = {}
        
        for k in range(top_k):
            results[output[k]['label']] = output[k]['score']
            
        return results
        
class ImageClassifier:
    """Classifies what objects appear in an image"""
    
    def __init__(self):
        self.model = None
    
    def init_model(self):
        from transformers import pipeline
        print("Loading image classification model...")
        self.model = pipeline('image-classification', 
                            model='google/vit-base-patch16-224')
        print("✓ Image classifier ready!")
    
    def process_query(self, image):
        results = self.model(image)
        top_result = results[0]
        
        return {
            'top_class': top_result['label'],
            'confidence': round(top_result['score'], 3),
            'top_5_predictions': [
                {
                    'label': r['label'],
                    'confidence': round(r['score'], 3)
                } for r in results[:5]
            ],
            'message': f"I'm {top_result['score']:.1%} sure this is: {top_result['label']}! 🎯"
        }
        
class TextSummarizer:
    """Summarizes long text into shorter versions"""
    
    def __init__(self):
        self.model = None
    
    def init_model(self):
        from transformers import pipeline
        print("Loading summarization model...")
        self.model = pipeline('summarization', 
                            model='facebook/bart-large-cnn')
        print("✓ Summarizer ready!")
    
    def process_query(self, text):
        # BART works best with 50-1024 tokens
        if len(text.split()) < 50:
            return {
                'summary': text,
                'original_length': len(text.split()),
                'summary_length': len(text.split()),
                'reduction': '0%',
                'message': 'Text is already short! No need to summarize. 📏'
            }
        
        # Generate summary
        max_length = min(130, len(text.split()) // 2)
        summary_result = self.model(text, 
                                   max_length=max_length, 
                                   min_length=30, 
                                   do_sample=False)
        summary = summary_result[0]['summary_text']
        
        original_words = len(text.split())
        summary_words = len(summary.split())
        reduction = round((1 - summary_words / original_words) * 100)
        
        return {
            'summary': summary,
            'original_length': original_words,
            'summary_length': summary_words,
            'reduction': f"{reduction}%",
            'message': f"Compressed from {original_words} to {summary_words} words ({reduction}% reduction)! ✂️"
        }
        
class JokeGenerator:
    """Generates jokes based on a topic"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
    
    def init_model(self):
        from transformers import pipeline
        print("Loading joke generator...")
        self.model = pipeline('text-generation', 
                            model='gpt2',
                            max_length=100)
        print("✓ Joke generator ready!")
    
    def process_query(self, topic):
        prompt = f"Here's a funny joke about {topic}: "
        
        # Generate with some creativity
        result = self.model(prompt, 
                          max_length=80,
                          num_return_sequences=1,
                          temperature=0.8,
                          do_sample=True)
        
        generated = result[0]['generated_text']
        # Extract just the joke part
        joke = generated.replace(prompt, '').strip()
        
        # If it's too short or weird, provide a fallback
        if len(joke) < 20:
            joke = f"Why did the {topic} cross the road? To get to the other side! (Classic!) 🐔"
        
        return {
            'joke': joke,
            'topic': topic,
            'message': f"Here's a joke about {topic}! 🎭"
        }
        
class HaikuWriter:
    """Writes haikus about any topic"""
    
    def __init__(self):
        self.model = None
    
    def init_model(self):
        from transformers import pipeline
        print("Loading haiku writer...")
        self.model = pipeline('text-generation', 
                            model='gpt2')
        print("✓ Haiku writer ready!")
    
    def process_query(self, topic):
        prompt = f"Write a haiku about {topic}:\n"
        
        result = self.model(prompt, 
                          max_length=60,
                          num_return_sequences=1,
                          temperature=0.7,
                          do_sample=True)
        
        generated = result[0]['generated_text']
        haiku = generated.replace(prompt, '').strip()
        
        # Extract first 3 lines
        lines = haiku.split('\n')[:3]
        haiku = '\n'.join(lines)
        
        # Fallback if generation fails
        if len(lines) < 3:
            haiku = f"{topic} whispers soft\nIn the gentle morning light\nPeace within my heart"
        
        return {
            'haiku': haiku,
            'topic': topic,
            'message': f"A haiku about {topic} 🌸"
        }
        
class WhyExplainer:
    """Explains 'why' something works the way it does"""
    
    def __init__(self):
        self.model = None
    
    def init_model(self):
        from transformers import pipeline
        print("Loading why explainer...")
        self.model = pipeline('text-generation', 
                            model='gpt2')
        print("✓ Why explainer ready!")
    
    def process_query(self, question):
        # Format the question
        if not question.lower().startswith('why'):
            question = f"Why {question}"
        
        prompt = f"Question: {question}\nAnswer: "
        
        result = self.model(prompt, 
                          max_length=150,
                          num_return_sequences=1,
                          temperature=0.7,
                          do_sample=True)
        
        generated = result[0]['generated_text']
        # Extract just the answer
        answer = generated.replace(prompt, '').strip()
        
        # Get first complete sentence
        sentences = answer.split('.')
        explanation = sentences[0] + '.' if sentences else answer
        
        return {
            'explanation': explanation,
            'question': question,
            'message': f"Here's an explanation! 💡"
        }