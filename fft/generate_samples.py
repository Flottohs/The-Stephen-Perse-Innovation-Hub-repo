"""
Generate sample audio files for testing the FFT analyzer
"""
import numpy as np
from scipy.io import wavfile

def create_beep(filename='beep.wav', frequency=440, duration=0.5):
    """Create a simple beep sound at specified frequency"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Simple sine wave
    audio = np.sin(2 * np.pi * frequency * t)
    
    # Apply envelope to avoid clicks
    envelope = np.sin(np.pi * t / duration)
    audio = audio * envelope
    
    # Convert to 16-bit PCM
    audio = (audio * 32767).astype(np.int16)
    
    wavfile.write(filename, sample_rate, audio)
    print(f"Created {filename} - {frequency} Hz beep")

def create_chord(filename='chord.wav', frequencies=[261.63, 329.63, 392.00], duration=1.0):
    """Create a chord with multiple frequencies (C major chord by default)"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Sum of sine waves
    audio = np.zeros_like(t)
    for freq in frequencies:
        audio += np.sin(2 * np.pi * freq * t)
    
    # Normalize
    audio = audio / len(frequencies)
    
    # Apply envelope
    envelope = np.sin(np.pi * t / duration)
    audio = audio * envelope
    
    # Convert to 16-bit PCM
    audio = (audio * 32767).astype(np.int16)
    
    wavfile.write(filename, sample_rate, audio)
    print(f"Created {filename} - Chord with frequencies {frequencies} Hz")

def create_complex_sound(filename='complex.wav', duration=0.5):
    """Create a more complex sound with multiple harmonics"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Fundamental frequency with harmonics
    fundamental = 220  # A3
    audio = np.zeros_like(t)
    
    # Add harmonics with decreasing amplitude
    for i in range(1, 8):
        amplitude = 1.0 / i
        audio += amplitude * np.sin(2 * np.pi * fundamental * i * t)
    
    # Normalize
    audio = audio / audio.max()
    
    # Apply envelope
    envelope = np.sin(np.pi * t / duration)
    audio = audio * envelope
    
    # Convert to 16-bit PCM
    audio = (audio * 32767).astype(np.int16)
    
    wavfile.write(filename, sample_rate, audio)
    print(f"Created {filename} - Complex sound with harmonics")

if __name__ == '__main__':
    print("Generating sample audio files...\n")
    
    # Simple beep at A440
    create_beep('beep.wav', 440, 0.5)
    
    # Higher pitched beep
    create_beep('beep_high.wav', 880, 0.5)
    
    # C major chord
    create_chord('chord.wav', [261.63, 329.63, 392.00], 1.0)
    
    # Complex sound with harmonics
    create_complex_sound('complex.wav', 0.5)
    
    print("\nAll sample files created successfully!")
    print("You can now upload these files to the FFT analyzer.")
