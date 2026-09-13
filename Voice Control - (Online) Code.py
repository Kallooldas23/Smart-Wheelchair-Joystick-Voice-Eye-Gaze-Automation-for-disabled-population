import speech_recognition as sr
import serial
import time
# Setup Serial communication with Arduino
arduino = serial . Serial (’/dev / ttyACM0 ’, 9600 , timeout =1) #
Adjust if needed
time . sleep (2) # Allow Arduino time to reset
r = sr . Recognizer ()
mic = sr . Microphone ()
print (" Please wait . Calibrating microphone ...")
with mic as source :
r . adjust_for_ambient_noise ( source , duration =5)
print (" Calibration complete . Say something !")
while True :
try:
with mic as source :
print ("\ nListening ...")
audio = r . listen ( source )
words = r . recognize_google ( audio ) . lower ()
print ( f" Recognized : { words }")
47 if " forward " in words or " front " in words :
arduino . write ( b’F’)
print (" Sent : F")
elif " backward " in words or " back " in words :
arduino . write ( b’B’)
print (" Sent : B")
elif " left side " in words or " left " in words :
arduino . write ( b’L’)
print (" Sent : L")
elif " right side " in words or " right " in words :
arduino . write ( b’R’)
print (" Sent : R")
elif " stop " in words or " hold " in words :
arduino . write ( b’S’)
print (" Sent : S")
else :
print ("No valid command found .")
except sr . UnknownValueError :
print (" Google Speech Recognition could not understand
audio ")
except sr . RequestError as e :
print ( f" Could not request results ; {e}")
