import pyaudio
import speech_recognition as sr

CHUNK = 4096
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 16000 
RECORD_SECONDS = nsec
WAVE_OUTPUT_FILENAME = wavfile_name
NFRAMES = int((RATE * RECORD_SECONDS) / CHUNK)

# initialize pyaudio
p = pyaudio.PyAudio()
getInputDevice(p)

print('opening stream...')
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK,
                input_device_index = 1)

frames = []

# discard first 1 second
for i in range(0, NFRAMES):
    data = stream.read(CHUNK)


for i in range(0, NFRAMES):
    data = stream.read(CHUNK)
    #print(data)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()