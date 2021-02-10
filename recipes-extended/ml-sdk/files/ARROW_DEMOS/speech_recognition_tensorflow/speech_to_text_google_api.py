#!/usr/bin/env python3

# NOTE: Requires PyAudio python package

import speech_recognition as sr
import webbrowser

WIKI_SEARCH_URL = "https://en.wikipedia.org/wiki/"
GOOGLE_URL = "https://www.google.com/"
YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query="

MAIN_KEYWORD = 'anil'
KEYWORD_1 = 'wikipedia'
KEYWORD_2 = 'youtube'
KEYWORD_3 = 'open google'
KEYWORD_4 = 'not'
KEYWORD_5 = 'search'


def callback(recognizer, audio):
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `recognizer.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `recognizer.recognize_google(audio)`
        recognized_words = recognizer.recognize_google(audio)
        print("Speech Recognition thinks you said : " + recognized_words)

        # convert char array output to lower case string for comparision
        words = "".join(recognized_words)
        words = words.lower()

        if MAIN_KEYWORD in words:
            print("Main Keyword detected...")
            search_query=""

            if KEYWORD_5 in words:
                search_query = words[words.find(KEYWORD_5) + len(KEYWORD_5):]

            if KEYWORD_4 in words:
                print("User denied Action...")
            else:
                if KEYWORD_1 in words:
                    print("Opening WikiPedia in browser...")
                    webbrowser.open(WIKI_SEARCH_URL+search_query, new=2)
                elif KEYWORD_2 in words:
                    print("Opening YouTube in browser...")
                    webbrowser.open(YOUTUBE_SEARCH_URL+search_query, new=2)
                elif KEYWORD_3 in words:
                    print("Opening Google in browser...")
                    webbrowser.open(GOOGLE_URL, new=2)

    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))


# obtain audio from the microphone
r = sr.Recognizer()

available_microphone_list = sr.Microphone.list_microphone_names()
print("Available Audio Devices : Index")

for idx, val in enumerate(available_microphone_list):
    print(val, " : ", idx)

while True:
    index = input("Which input (audio) device you want? Please provide index value (in number) : ")
    if index.isnumeric() and int(index) < len(available_microphone_list):
        print("You selected audio device : ", index)
        break
    else:
        print("Please provide correct Numeric value only")

mic = sr.Microphone(device_index=int(index))

#with mic as source:
#    r.adjust_for_ambient_noise(source, duration=1)

# start listening in the background
stop_listening = r.listen_in_background(mic, callback, phrase_time_limit=3)

# `stop_listening` is now a function that, when called, stops background listening
# stop_listening(wait_for_stop=False)

input("Say Something Now!. It will continuously convert speech to text and Wait till 'ENTER' pressed...\n")
