# Audio FFT Analyzer - CS Club Educational Tool

A simple Flask web application that demonstrates how any audio can be decomposed into sine waves using Fast Fourier Transform (FFT).

## Features

- Upload audio files (.wav format)
- Performs FFT to extract frequency components
- Displays top 30 most significant sine waves
- Shows frequency, equation, and visual plot for each component
- Scrollable list of results
- Clean, educational interface

## Installation

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload a .wav audio file (like "beep.wav" or "oink.wav")

4. Click "Analyze Audio" to see the FFT decomposition

## How It Works

The application:
1. Reads the uploaded audio file
2. Performs Fast Fourier Transform (FFT) using `scipy.fft`
3. Extracts the top 30 frequency components by magnitude
4. For each component, generates:
   - The frequency in Hz
   - The sine wave equation: `y(t) = magnitude * sin(2π * frequency * t + phase)`
   - A visual plot of the sine wave

## Educational Value

This tool demonstrates the fundamental concept that any periodic signal (including audio) can be represented as a sum of sine waves at different frequencies, amplitudes, and phases. This is the basis of Fourier analysis and is crucial in:

- Audio processing
- Signal analysis
- Music synthesis
- Compression algorithms
- And many other applications

## Example Audio Files

You can create simple test files using Python:

```python
import numpy as np
from scipy.io import wavfile

# Create a simple beep at 440 Hz (A note)
sample_rate = 44100
duration = 1.0
t = np.linspace(0, duration, int(sample_rate * duration))
beep = np.sin(2 * np.pi * 440 * t)
wavfile.write('beep.wav', sample_rate, (beep * 32767).astype(np.int16))
```

## Notes

- Only .wav files are supported
- Maximum file size: 16MB
- The app displays 50ms of each sine wave for clarity
- Components are ordered by magnitude (strongest to weakest)
