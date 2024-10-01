import os
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import  requests
import sys
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "creds.json"


def cria_audio(audio, msg, lang="pt-br"):
    tts = gTTS(msg, lang=lang)
    tts.save(audio)
    playsound(audio)
    os.remove(audio)


# cria_audio('audios/welcome.mp3', "Olá eu sou Ana. Em que posso ajudar")


def monitora_audio():
    recon = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print('diga algo')
            audio = recon.listen(source)            
            try:
                msg = recon.recognize_google_cloud(audio, language="pt-BR")
                msg = msg.lower()
                print('voce disse: ', msg)
                executa_comandos(msg)
                break
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
            
            # except Exception as e:
            #     print(e)
        return msg
    

def executa_comandos(mensagem):
    if 'fechar assistente' in mensagem:
        sys.exit()

# :if __name__ == "__main__":
    # monitora_audio()

def main():
    cria_audio('audios/welcome.mp3', "Olá eu sou Ana. Em que posso ajudar")

    # playsound('audios/bemvindo.wav')
    while True:
        monitora_audio()

main()