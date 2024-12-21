import speech_recognition as sr
from fuzzywuzzy import process
from gradio_client import Client
import os
import simpleaudio as sa
from database_connect import get_item_list

r = sr.Recognizer() 

def SpeakText(text):
    '''
    speak the text
    '''
    client = Client("mrfakename/MeloTTS", download_files='./')
    result = client.predict(
        text=text,
        speaker="EN-US",
        speed=1,
        language="EN",
        api_name="/synthesize"
    )
    path=result.split('\\')[-2]
    os.rename(f'.\{path}\\audio', f'.\{path}\\output.wav')
    play_audio(f'.\{path}\\output.wav')     # Play the file using playsound
    # os.remove(f".\{path}") # Delete the file after playing

def similarity(text, item_list, threshold=80):
    '''
    to find the similarity of the text input and return the name in the list if sim. > 80%
    '''
    word,ratio = process.extractOne(text,item_list)
    if ratio > threshold:
        return word
    return None

def play_audio(path):
    '''
    play the audio file
    '''
    wave_obj = sa.WaveObject.from_wave_file(path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def speak_item(item_list):
    test=None
    '''
    keep detecting user's speech until the item name is spoken
    '''
    noItem=True
    play_audio('audio/intro.wav')
    while noItem:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)
                text = r.recognize_google(audio).lower()
                print(text)
                test=similarity(text,item_list)
                if test:
                    SpeakText(f'Got it, we have {test} in the supermarket')
                    return test
        except sr.UnknownValueError:
            play_audio('audio/again.wav')