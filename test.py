from gradio_client import Client
import os
import simpleaudio as sa

client = Client("mrfakename/MeloTTS", download_files='./')
result = client.predict(
    text="Please turn right",
    speaker="EN-US",
    speed=0.8,
    language="EN",
    api_name="/synthesize"
)
path=result.split('\\')[-2]
os.rename(f'.\{path}\\audio', f'.\{path}\\output.wav')

# Play the file using playsound
wave_obj = sa.WaveObject.from_wave_file(f'.\{path}\\output.wav')
play_obj = wave_obj.play()
play_obj.wait_done()

# Delete the file after playing
os.remove(f".\{path}")

