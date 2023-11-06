import speech_recognition as sr
import pyttsx3

def text_to_voice(msg):
    answer = pyttsx3.init()
    answer.say(msg)
    answer.runAndWait()
    
def console_print_say(msg):
    print(msg + "\n")
    text_to_voice(msg)

def recognize_voice():
    # Initialize recognizer
    voice_recognizer = sr.Recognizer()

    # Use microphone as source
    with sr.Microphone() as source:
        voice_recognizer.adjust_for_ambient_noise(source)
        # print("Escuchando...")
        audio = voice_recognizer.listen(source)

    # Recognize speech using Google Speech Recognition
    try:
        print("Reconociendo...")
        query = voice_recognizer.recognize_google(audio, language='es-PE')
        print(f"Has dicho {query}\n")
    except sr.RequestError:
        print("Hubo un error(externo) con la solicitud de reconocimiento")
    except sr.UnknownValueError:
        print("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado")

    return query.lower()
