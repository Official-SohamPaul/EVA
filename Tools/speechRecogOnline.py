import speech_recognition as sr
import pyaudio

def recognize():
    #initialize the recognizer
    recognizer=sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.pause_threshold=1
        audio=recognizer.listen(source,0,8)
    try:
        print('Recognizing....')
        quary=recognizer.recognize_google(audio,language='en')
        print('\nUSER: '+quary.lower())
        return str(quary).lower()
    except Exception :
        return None
    
# Driver Code 
# print(recognize())