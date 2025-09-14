# check_mic.py
import speech_recognition as sr

print("Micrófonos disponibles:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f'[{index}] "{name}"')