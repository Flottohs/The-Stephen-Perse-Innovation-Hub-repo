from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
from io import BytesIO
from PIL import Image
import tools

app = Flask(__name__)
CORS(app)

# Initialize all tools at startup
tool_instances = {
    'semantics': tools.SemanticsAnalyzer(),
    'classifier': tools.ImageClassifier(),
    # 'summarizer': tools.TextSummarizer(),
    'quest': tools.RPGQuestGenerator(),
    'haiku': tools.HaikuWriter(),
    'explainer': tools.WhyExplainer()
}

# Initialize models for all tools
print("🚀 Initializing AI models...")
for name, tool in tool_instances.items():
    print(f"  Loading {name}...")
    tool.init_model()
print("✅ All models ready!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process():
    try:
        data = request.json
        tool_name = data.get('tool')
        input_type = data.get('type')  # 'text' or 'image'
        content = data.get('content')
        
        if tool_name not in tool_instances:
            return jsonify({'error': 'Unknown tool or tool not initialized'}), 400
        
        tool = tool_instances[tool_name]
        
        # Process based on input type
        if input_type == 'image':
            # Decode base64 image
            image_data = base64.b64decode(content.split(',')[1])
            image = Image.open(BytesIO(image_data))
            # Ensure image is loaded and in RGB mode
            image = image.convert('RGB')
            result = tool.process_query(image)
        else:
            result = tool.process_query(content)
        
        return jsonify({'result': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)