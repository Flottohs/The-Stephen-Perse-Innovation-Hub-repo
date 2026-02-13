from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import base64
from io import BytesIO
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store latest analysis results globally for save and mixer functionality
latest_results = None
latest_sample_rate = None

def analyze_audio(file_path):
    """Perform FFT on audio file and extract top sine wave components"""
    
    # Read the audio file
    sample_rate, data = wavfile.read(file_path)
    
    # Convert to mono if stereo
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    
    # Perform FFT
    n = len(data)
    yf = fft(data)
    xf = fftfreq(n, 1 / sample_rate)
    
    # Get positive frequencies only
    positive_freq_idx = xf > 0
    xf = xf[positive_freq_idx]
    yf = yf[positive_freq_idx]
    
    # Get magnitudes
    magnitudes = np.abs(yf)
    
    # Find top 30 frequencies by magnitude
    top_indices = np.argsort(magnitudes)[-30:][::-1]
    
    results = []
    for idx in top_indices:
        frequency = xf[idx]
        magnitude = magnitudes[idx]
        phase = np.angle(yf[idx])
        
        # Generate sine wave plot
        t = np.linspace(0, 0.05, 1000)  # 50ms of signal
        sine_wave = magnitude * np.sin(2 * np.pi * frequency * t + phase)
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(t, sine_wave, 'b-', linewidth=2)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.set_title(f'Frequency: {frequency:.2f} Hz')
        ax.grid(True, alpha=0.3)
        
        # Convert plot to base64
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=80, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        # Create equation string
        equation = f"y(t) = {magnitude:.2f} * sin(2π * {frequency:.2f} * t + {phase:.2f})"
        
        results.append({
            'frequency': frequency,
            'magnitude': magnitude,
            'equation': equation,
            'plot': img_base64
        })
    
    return results, sample_rate

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    global latest_results, latest_sample_rate
    
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['audio_file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save the file temporarily
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
    file.save(file_path)
    
    try:
        results, sample_rate = analyze_audio(file_path)
        
        # Store results globally for save and mixer features
        latest_results = results
        latest_sample_rate = sample_rate
        
        return jsonify({
            'success': True,
            'sample_rate': int(sample_rate),
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.route('/save-results', methods=['GET'])
def save_results():
    """Save all graphs and equations to a PDF file"""
    global latest_results, latest_sample_rate
    
    if not latest_results:
        return jsonify({'error': 'No results to save'}), 400
    
    try:
        from matplotlib.backends.backend_pdf import PdfPages
        
        # Create PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f'fft_results_{timestamp}.pdf')
        
        with PdfPages(pdf_path) as pdf:
            # Title page
            fig = plt.figure(figsize=(11, 8.5))
            fig.text(0.5, 0.7, 'Audio FFT Analysis Results', 
                    ha='center', fontsize=24, fontweight='bold')
            fig.text(0.5, 0.6, f'Sample Rate: {latest_sample_rate} Hz', 
                    ha='center', fontsize=14)
            fig.text(0.5, 0.5, f'Top 30 Sine Wave Components', 
                    ha='center', fontsize=14)
            fig.text(0.5, 0.4, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
                    ha='center', fontsize=12, style='italic')
            plt.axis('off')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
            
            # Create pages with graphs and equations
            for idx, result in enumerate(latest_results):
                fig, ax = plt.subplots(figsize=(11, 8.5))
                
                # Regenerate the sine wave
                frequency = result['frequency']
                magnitude = result['magnitude']
                phase = np.angle(complex(result.get('real', 1), result.get('imag', 0))) if 'real' in result else 0
                
                t = np.linspace(0, 0.05, 1000)
                sine_wave = magnitude * np.sin(2 * np.pi * frequency * t + phase)
                
                # Plot
                ax.plot(t, sine_wave, 'b-', linewidth=2)
                ax.set_xlabel('Time (s)', fontsize=12)
                ax.set_ylabel('Amplitude', fontsize=12)
                ax.set_title(f'Component #{idx + 1} - Frequency: {frequency:.2f} Hz', 
                           fontsize=16, fontweight='bold', pad=20)
                ax.grid(True, alpha=0.3)
                
                # Add equation as text
                equation_text = result['equation']
                ax.text(0.5, -0.15, equation_text, 
                       transform=ax.transAxes, 
                       fontsize=11, 
                       ha='center',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
                
                plt.tight_layout()
                pdf.savefig(fig, bbox_inches='tight')
                plt.close(fig)
        
        # Send the file
        return send_file(pdf_path, 
                        as_attachment=True, 
                        download_name=f'fft_results_{timestamp}.pdf',
                        mimetype='application/pdf')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/mix-audio', methods=['POST'])
def mix_audio():
    """Create audio from selected sine wave components"""
    global latest_results, latest_sample_rate
    
    if not latest_results:
        return jsonify({'error': 'No results available'}), 400
    
    try:
        data = request.json
        selected_indices = data.get('selected_indices', [])
        
        if not selected_indices:
            return jsonify({'error': 'No components selected'}), 400
        
        # Audio parameters
        duration = 2.0  # 2 seconds
        sample_rate = latest_sample_rate or 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Mix selected sine waves
        mixed_audio = np.zeros_like(t)
        
        for idx in selected_indices:
            if 0 <= idx < len(latest_results):
                result = latest_results[idx]
                frequency = result['frequency']
                magnitude = result['magnitude']
                phase = np.angle(complex(result.get('real', 1), result.get('imag', 0))) if 'real' in result else 0
                
                # Add this component
                mixed_audio += magnitude * np.sin(2 * np.pi * frequency * t + phase)
        
        # Normalize to prevent clipping
        if mixed_audio.max() > 0:
            mixed_audio = mixed_audio / mixed_audio.max() * 0.8
        
        # Apply fade in/out to avoid clicks
        fade_samples = int(0.01 * sample_rate)  # 10ms fade
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        mixed_audio[:fade_samples] *= fade_in
        mixed_audio[-fade_samples:] *= fade_out
        
        # Convert to 16-bit PCM
        audio_int16 = (mixed_audio * 32767).astype(np.int16)
        
        # Save to temporary file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], f'mixed_audio_{timestamp}.wav')
        wavfile.write(audio_path, sample_rate, audio_int16)
        
        # Read file and convert to base64
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        # Clean up
        os.remove(audio_path)
        
        return jsonify({
            'success': True,
            'audio_data': audio_base64,
            'num_components': len(selected_indices)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
