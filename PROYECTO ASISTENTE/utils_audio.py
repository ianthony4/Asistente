import speech_recognition as sr
import pyttsx3

def text_to_voice(sentence):
    answer = pyttsx3.init()
    answer.say(sentence)
    answer.runAndWait()
    
def console_print_say(phrase_array):
    if type(phrase_array) is str:
        console_print_say_string(phrase_array)
        return
    
    for sentence in phrase_array:
        console_print_say_string(sentence)

def console_print_say_string(sentence):
    print(sentence + " "),
    # text_to_voice(sentence)

def recognize_voice():
    query = input()
    # # Initialize recognizer
    # voice_recognizer = sr.Recognizer()
    # query = None

    # # Use microphone as source
    # with sr.Microphone() as source:
    #     voice_recognizer.adjust_for_ambient_noise(source)
    #     print("Escuchando...")
    #     audio = voice_recognizer.listen(source)

    # # Recognize speech using Google Speech Recognition
    # try:
    #     print("Reconociendo...")
    #     query = voice_recognizer.recognize_google(audio, language='es-PE')
    #     print(f"Has dicho {query}\n")
    # except sr.RequestError:
    #     print("Hubo un error(externo) con la solicitud de reconocimiento")
    #     query = input()
    # except sr.UnknownValueError:
    #     print("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado")
    #     query = input()

    return query.lower()
