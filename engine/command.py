import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from gtts import gTTS
import os
import eel
import time
from engine.featuresengine.features import openCommand
from engine.features import PlayYoutube, findContact, whatsApp, makeCall, sendMessage, chatBot

# Load Wav2Vec2.0 Model
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

# Function for TTS using gTTS
def speak(text):
    text = str(text)
    print(f"Assistant: {text}")
    eel.DisplayMessage(text)
    tts = gTTS(text, lang='en')
    tts.save("response.mp3")
    os.system("start response.mp3")  # For Windows, use 'start'
    eel.receiverText(text)

# Function for STT using Wav2Vec 2.0
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)
    
    try:
        print('recognizing...')
        eel.DisplayMessage('recognizing...')
        
        # Convert speech to text
        audio_data = torch.tensor(audio.get_raw_data())
        input_values = tokenizer(audio_data, return_tensors="pt", padding="longest").input_values
        logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        query = tokenizer.batch_decode(predicted_ids)[0].lower()

        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        return query
    except Exception as e:
        return ""

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:
        if "open" in query:
            from engine.featuresengine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use, WhatsApp or mobile?")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("What message to send?")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again.")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("What message to send?")
                        query = takecommand()
                                                    
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                                    
                    whatsApp(contact_no, query, message, name)

        else:
            from engine.features import chatBot
            chatBot(query)
    except Exception as e:
        print(f"Error: {e}")
    
    eel.ShowHood()
