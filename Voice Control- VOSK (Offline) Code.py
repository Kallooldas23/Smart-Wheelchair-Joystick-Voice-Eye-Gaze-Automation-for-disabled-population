from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
import serial
model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)
arduino = serial.Serial(’/dev/ttyUSB0’, 9600)
def callback(indata, frames, time, status):
if rec.AcceptWaveform(indata):
result = json.loads(rec.Result())
command = result.get("text", "")
print(command)
if "forward" in command:
arduino.write(b’F’)
elif "backward" in command:
arduino.write(b’B’)
elif "left" in command:
arduino.write(b’L’)
elif "right" in command:
arduino.write(b’R’)
elif "stop" in command:
arduino.write(b’S’)
76
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype=’
int16’, channels=1, callback=callback):
print("Listening...")
while True:
pass
