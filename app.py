import assemblyai as aai
import os
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import  requests
import sys
from  dotenv import load_dotenv

#carregando as variaveis de ambiente registradas no .env
load_dotenv()

#variaveis de ambiente 
aai.settings.api_key = os.environ['ASSEMBLYAI_API_KEY']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "creds.json"


def on_open(session_opened: aai.RealtimeSessionOpened):
    print('Session_id', session_opened.session_id)


def on_data(transcript: aai.RealtimeTranscript):
    
    if not transcript:
        return
    if isinstance( transcript, aai.RealtimeFinalTranscript):
        print(transcript.text, end='\r\n')
    else:
        print(transcript.text, end='\r')

def on_error(error: aai.RealtimeError):
    print('An error', error)


def on_close():
    print("fechando")

config = aai.TranscriptionConfig(language_code='pt', speaker_labels=True)
trascriber  = aai.Transcriber()
trascriber_real = aai.RealtimeTranscriber(
    sample_rate=16_000,
    on_data=on_data,
    on_error=on_error,
    on_open=on_open,
    on_close=on_close

)
trascriber_real.connect()

mic = aai.extras.MicrophoneStream(sample_rate=16_000)

# transcript = trascriber.transcribe('audios/welcome.mp3', config)
# transcript = trascriber.transcribe(mic , config)
trascriber_real.stream(mic)

trascriber_real.close()


# for  it in transcript.utterances:
#     print(f'Speaker {it.speaker}: {it.text}')

# print(transcript.text)


def cria_audio(audio, msg, lang="pt-br"):
    tts = gTTS(msg, lang=lang)
    tts.save(audio)
    playsound(audio)
    os.remove(audio)


# cria_audio('audios/welcome.mp3', "Olá eu sou Ana. Em que posso ajudar\
            # qual seria seu nome? ")


def monitora_audio():
    recon = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print('diga algo')
            audio = recon.listen(source)

            try:
                recon.adjust_for_ambient_noise(source)
                
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

# def main():
#     # cria_audio('audios/welcome.mp3', "Olá eu sou Ana. Em que posso ajudar")

#     # playsound('audios/bemvindo.wav')
#     while True:
#         monitora_audio()

# main()