# 🛠️ AI Toolkit Lab - Y11 Club Session

A collaborative AI project where each student implements one tool!

## 🎯 The Goal

Build a working AI toolkit by implementing different AI-powered tools. Each student picks one tool and implements just 2 functions. Then we put them all together!

## 📦 Setup

### 1. Install Dependencies

```bash
pip install flask flask-cors pillow transformers torch
```

### 2. Run the Server

```bash
python app.py
```

### 3. Open Your Browser

Go to: `http://localhost:5000`

## 👨‍💻 How to Implement Your Tool

Open `tools.py` and find your tool class. You need to implement 2 functions:

### Function 1: `init_model()`
This runs ONCE when the server starts. Load your AI model here.

### Function 2: `process_query(input)`
This runs every time someone uses your tool. Process the input and return results.

## 📝 Example Implementation

Here's a complete example for the **Semantics Analyzer**:

```python
class SemanticsAnalyzer:
    """Analyzes the semantic meaning and sentiment of text"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
    
    def init_model(self):
        """Load the sentiment analysis model"""
        from transformers import pipeline
        print("Loading sentiment analysis model...")
        self.model = pipeline('sentiment-analysis', 
                            model='distilbert-base-uncased-finetuned-sst-2-english')
        print("✓ Sentiment model ready!")
    
    def process_query(self, text):
        """Analyze text sentiment"""
        # Run the model
        result = self.model(text)[0]
        
        # Format the output
        return {
            'sentiment': result['label'].lower(),
            'confidence': round(result['score'], 3),
            'text_length': len(text),
            'message': f"This text is {result['label'].lower()} with {result['score']:.1%} confidence"
        }
```

## 🔧 Tool Suggestions

### For Sentiment Analyzer
- Model: `pipeline('sentiment-analysis')`
- Return: sentiment, confidence score

### For Image Classifier
- Model: `pipeline('image-classification')`
- Return: top classes, confidence scores

### For Summarizer
- Model: `pipeline('summarization', model='facebook/bart-large-cnn')`
- Return: summary text, compression ratio

### For Joke Generator
- Model: `pipeline('text-generation', model='gpt2')`
- Prompt: f"Write a funny joke about {topic}:"
- Return: generated joke

### For Haiku Writer
- Model: `pipeline('text-generation', model='gpt2')`
- Prompt: f"Write a haiku about {topic} in 5-7-5 format:"
- Return: haiku (you might need to extract the first 3 lines)

### For Why Explainer
- Model: `pipeline('text-generation', model='gpt2')`
- Prompt: f"Question: {question}\nAnswer:"
- Return: explanation

## 💡 Pro Tips

1. **Start small**: Use simple models like 'distilbert' or 'gpt2'
2. **Test incrementally**: Implement `init_model()` first, test it loads
3. **Check output shapes**: Print what your model returns to understand the format
4. **Handle errors**: Wrap your code in try/except if you want
5. **Add personality**: Make your return messages fun!

## 🎮 Testing Your Tool

1. Start the server: `python app.py`
2. Click on your tool in the web interface
3. Enter some test input
4. Click "Run Tool"
5. Check if it works!

## 🚀 Assembly Time (~5 mins)

Once everyone is done:
1. One person creates a new `tools.py` file
2. Copy-paste each student's implementation
3. Run the server
4. Test all tools together!

## ⚠️ Common Issues

**Model won't load:**
- Check your internet connection (models download on first use)
- Try a smaller model
- Check the model name is correct

**"Not implemented" message:**
- Make sure you removed the placeholder `pass` statement
- Check your indentation (Python is picky!)

**Weird results:**
- Print what your model returns: `print(result)`
- Check the model's output format in the transformers docs

## 📚 Resources

- Transformers docs: https://huggingface.co/docs/transformers
- Model hub: https://huggingface.co/models
- Pipeline guide: https://huggingface.co/docs/transformers/main_classes/pipelines

Have fun! 🎉
