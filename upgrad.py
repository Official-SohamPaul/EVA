import pyaudio
import numpy as np

# Constants
CHUNK = 8  # Number of frames per buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Sample rate in Hz
THRESHOLD = 600  # Adjust according to your environment

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Listening for claps...")

try:
    while True:
        # Read audio data
        data = stream.read(CHUNK)
        
        # Convert data to numpy array
        numpy_data = np.frombuffer(data, dtype=np.int16)
        
        # Calculate the average amplitude
        amplitude = np.abs(numpy_data).mean()
        
        # Check if amplitude exceeds the threshold
        if amplitude > THRESHOLD:
            print("Clap detected!")
            
            
except KeyboardInterrupt:
    print("Stopped by user")

# Close the stream
stream.stop_stream()
stream.close()
audio.terminate()
