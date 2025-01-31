import speech_recognition as sr
from fuzzywuzzy import process
from gradio_client import Client
import os
import simpleaudio as sa
from database_connect import get_item_list
import shutil

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

    norm_path = os.path.normpath(result) # normalise the file path
    path = norm_path.split(os.path.sep)[-2] # obtain the folder name containing the audio file

    source_file = os.path.join('.', path, 'audio')
    dest_file = os.path.join('.', path, 'output.wav')
    os.rename(source_file, dest_file)

    play_audio(dest_file)

    shutil.rmtree(os.path.join('.', path), ignore_errors=True) # Delete the file after playing


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