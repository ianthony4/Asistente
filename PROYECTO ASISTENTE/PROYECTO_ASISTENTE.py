import speech_recognition as sr
import pyttsx3
import time
import sys
import tkinter as tk
import random
import json
from tkinter import messagebox
from PIL import Image, ImageTk

tema = "Ejecucion de Instrucciones"
# (NO TOCAR) CONVERTIR CADENAS DE TEXTO A AUDIO Y REPRODUCIRLAS 
def texto_a_audio(comando):
    palabra = pyttsx3.init()
    palabra.say(comando)
    palabra.runAndWait()

# (NO TOCAR) CAPTURA AUDIO DESDE EL MICROFONO Y ANALIZA POSIBLES ERRORES
def capturar_voz(reconocer, microfono, tiempo_ruido = 1.0):
    if not isinstance(reconocer, sr.Recognizer):
        raise TypeError("'reconocer' no es de la instacia 'Recognizer'")

    if not isinstance(microfono, sr.Microphone):
        raise TypeError("'reconocer' no es de la instacia 'Recognizer'")
    
    with microfono as fuente:
        reconocer.adjust_for_ambient_noise(fuente, duration = tiempo_ruido)
        audio = reconocer.listen(fuente)
    respuesta = {
        "suceso": True,
        "error": None,
        "mensaje": None,
    }
    try:
        respuesta["mensaje"] = reconocer.recognize_google(audio, language="es-PE")
    except sr.RequestError:
        respuesta["suceso"] = False
        respuesta["error"] = "API no disponible"
    except sr.UnknownValueError:
        respuesta["error"] = "Habla inteligible"
    return respuesta
# (NO TOCAR) Adicional - Escribe en consola y el bot lo lee
def consolesay(str):
    print(str+"\n")
    texto_a_audio(str)
# (NO TOCAR) CONVIERTE A UNA CADENA DE TEXTO EN MINUSCULA EL AUDIO ENVIADO POR MICROFONO
def enviar_voz():
    while (1):
        palabra = capturar_voz(recognizer, microphone)
        if palabra["mensaje"]:
            break
        if not palabra["suceso"]:
            print("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado. <", nombre["error"],">")
            texto_a_audio("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado.")
            exit(1)
        consolesay("No pude escucharte, ¿podrias repetirlo?")
    return palabra["mensaje"].lower()

# (NO TOCAR) BASE DE DATOS DONDE SE ENCUENTRA TODA LA INFORMACION CONCERNIENTE

with open('basedatos.json', 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)
#Acceder a la parte especifica que se desea imprimir
# (MODIFICABLE) VARIABLES PARA MEJORAR EL CODIGO - ANTHONY
opciones = "\n1) Lectura\n 2) Decodificacion\n 3) Ejecucion \n 4) Almacenamiento\n 5) Ejemplos"
mainMenu = "\n1) Aprendizaje\n2) Test\n3) Juegos\n"
menu2 = "\n1) Cronograma instruccion agregar (ADD)\n2) Ejecucion de la instruccion SW \n3) Ejecucion de la instruccion JWZ"
menuadd = "\n1) Fase de Busqueda \n2) Fase de busqueda de operandos\n3)Fase de ejecucion y almacenamiento del resultado"
siono = "Responde con:\n1) Bien.\n2) Regresar \n3) No gracias"
# (MODIFICABLE) Funciones - Anthony para evitar la reutilizacion de codigo
def continuar(menu):
    consolesay("¿Quieres seguir aprendiendo?")
    time.sleep(0.5)
    print(siono)
    respuesta = enviar_voz()
    print("Tu respuesta " + respuesta)
    #COMPRUEbA QUE EL MENSAJE ENVIADO SEA VALIDO
    if respuesta == "bien": 
        #ELEGIMOS CON QUÉ OPCIÓN SEGUIR
        consolesay("Elige la opcion que desees aprender: ")
        print(menu)
        return True
    elif respuesta == "no gracias":
        consolesay("Oh. es una lástima. En ese caso nos veremos en otra ocasión")                        
        time.sleep(0.5)
        consolesay("Espero que hayas aprendido mucho sobre este tema. Hasta luego.")
        exit(0)
    #SI EL MENSAJE ENVIADO NO ES ERRONEO LE PIDE AL USUARIO SELECCIONAR UNA OPCION VALIDA
    else:
        consolesay(nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
        print(siono)

def still():
    consolesay("¿Quieres seguir aprendiendo?")
    time.sleep(0.5)
    print(siono)
    respuesta = enviar_voz()
    print("Tu respuesta " + respuesta)
    #COMPRUEbA QUE EL MENSAJE ENVIADO SEA VALIDO
    if respuesta == "bien": 
        #ELEGIMOS CON QUÉ OPCIÓN SEGUIR
        consolesay("Elige la opcion que desees aprender: ")
        return True
    elif respuesta == "regresar": 
        #ELEGIMOS CON QUÉ OPCIÓN SEGUIR
        consolesay("Elige la opcion que desees aprender: ")
        return False
    elif respuesta == "no gracias":
        consolesay("Oh. es una lástima. En ese caso nos veremos en otra ocasión")                        
        time.sleep(0.5)
        consolesay("Espero que hayas aprendido mucho sobre este tema. Hasta luego.")
        exit(0)
    #SI EL MENSAJE ENVIADO NO ES ERRONEO LE PIDE AL USUARIO SELECCIONAR UNA OPCION VALIDA
    else:
        not_recognized()
        print(siono)

def not_recognized():
    consolesay(nombre + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
    consolesay("Responde con una de las alternativas mencionadas.")
    return False

# Aspectos necesarios para la fase TEST
# Variables para la fase TEST
puntos = 0

# Métodos para la fase de test
def aumentarPuntos():
    global puntos
    puntos += 1
    print("TU PUNTAJE ES DE " + str(puntos) + " PUNTO/s")
                    
def escribir_respuesta(pregunta, alternativas, respuesta_correcta):
    print(pregunta)
    for i, alternativa in enumerate(alternativas, start = 1):
        print(f"{i}. {alternativa}")        
    respuesta_usuario = input("Escribe el número de la alternativa que crees correcta: ")
    if respuesta_usuario.isdigit():
        opcion_elegida = int(respuesta_usuario)
    else:
        print("Entrada inválida. Por favor, ingresa el número de la alternativa.")
        return

    if not 1 <= opcion_elegida <= len(alternativas):
        print("Opción inválida.")
        return
                        
    if alternativas[opcion_elegida - 1] == respuesta_correcta:
        consolesay("¡Respuesta correcta!")
        aumentarPuntos()
    else:
        consolesay("Respuesta incorrecta.")

def mostrar_pregunta(enunciado):
    consolesay(enunciado["pregunta"][0])
    for i, alternativa in enumerate(enunciado["alternativas"], start = 0):
        print(f"{chr(97 + i)}) {alternativa}")
    respuesta_usuario = enviar_voz()
    print("Tu respuesta " + respuesta_usuario)
    if respuesta_usuario.lower() == enunciado["respuesta"][0].lower():
        consolesay("¡Respuesta correcta!")
        aumentarPuntos()
    else:
        consolesay("Respuesta incorrecta")
    
        

#INICIO
if __name__ == "__main__":

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    salir = False

    #USANDO LA FUNCIÓN TEXTO_A_AUDIO SE HACE LEER CADENAS DE TEXTO, COMO SI LA COMPUTADORA TE ESTUVIERA HABLANDO
    texto_a_audio(datos['bienvenida'])
    print("Di tu nombre: ")
    #LA FUNCION 'enviar_voz' RETORNA UNA CADENA DE TEXTO DEL AUDIO ENVIADO POR VOZ DEL USUARIO
    nombre = enviar_voz()
    consolesay("Hola {}. Mucho gusto.".format(nombre))
    consolesay("{} Ahora voy a explicarte sobre las opciones que tiene este programa. Tienes 3 opciones para escoger.".format(nombre))
    texto_a_audio("Aprendizaje. Tests. Juegos.")
    consolesay("La opción Aprendizaje es donde podrás aprender todo con respecto a la "+tema+". La opción Tests es donde podrás poner en práctica lo que aprendiste mediante exámenes. Y por último, la tercer opción, es Juegos, donde tambien podrás demostrar lo que aprendiste jugando.")
    consolesay("¿Qué opción eliges?")
    time.sleep(0.1)
    texto_a_audio("¿Aprendizaje? ¿Tests? ¿Juegos?")
    #SE USA LA FUNCION SLEEP DE LA LIBRERIA TIME PARA PAUSAR UN TIEMPO LA EJECUCION DEL PROGRAMA
    #PARA QUE LA INTERACCION SEA MAS NATURAL
    time.sleep(0.1)
    #PREGUNTA AL USUARIO QUE OPCION ELIGE
    while (1): 
        print(mainMenu)
        respuesta = enviar_voz()
        print("Tu respuesta " + respuesta)
        if respuesta == "aprendizaje": 
            consolesay("Elegiste la opcion APRENDIZAJE.")
            consolesay("Muy bien, empecemos entonces.")
            consolesay("Antes de empezar quisiera hacer una introduccion a la "+tema+".")
            time.sleep(0.5)
            class ImageWindow:
                def __init__(self, root, image_path):
                    self.root = root
                    self.root.title("Imagen")                   
                    self.image = Image.open(f"imgs/{image_path}") #SE CAMBIO LA RUTA DE LAS IMAGENES PARA UNA MEJOR ORGANIZACION
                    self.tk_image = ImageTk.PhotoImage(self.image)                   
                    self.image_label = tk.Label(root, image=self.tk_image)
                    self.image_label.pack()                   
                def update(self):
                    # Actualizar la ventana (puedes agregar lógica de actualización aquí si es necesario)
                    self.root.update_idletasks()
                    self.root.after(100, self.update)  # Llama a la función de actualización cada 100 ms
            def main():
                root = tk.Tk()
                image_path = "intro.png"  # Ruta de la imagen que deseas abrir               
                image_window = ImageWindow(root, image_path)
                image_window.update()  # Iniciar la función de actualización
                root.mainloop()
            if __name__ == "__main__":
                main()
            texto_a_audio(datos['aprendizaje'])           
            def mostrarImagen(str): #Método para mostrar imagen probara usando .png o .jpg
                extension = ".jpg"
                extension2 = ".png"
                try:
                    img = Image.open(f"imgs/{str+extension}")
                except:
                    img = Image.open(f"imgs/{str+extension2}")
                size = (600,400)
                img = img.resize(size)
                img.show()
            def ejecutar(str): # Método que muestra, imprime y habla
                mostrarImagen(str)
                texto_a_audio(datos[str])
            #FASES
            ejecutar("fases")
            #PREGUNTA AL USUARIO CON QUÉ PARTE DESEA EMPEZAR
            while(not salir):
                print(opciones)
                consolesay("¿Por cual deseas empezar?")
                time.sleep(0.5)
                #COMPRUEBA QUE EL MENSAJE ENVIADO SEA VALIDO
                respuesta = enviar_voz()
                print("Tu respuesta " + respuesta)
                if respuesta == "lectura":
                    ejecutar(respuesta)
                    #Si o No para continuar                     
                elif respuesta == "decodificación": 
                    ejecutar("decodificacion") #No posible por la coma
                elif respuesta == "ejecución":
                    ejecutar("ejecucion") #No posible por la coma       
                elif respuesta == "almacenamiento":
                    ejecutar(respuesta)
                elif respuesta == "ejemplos":
                    while(not salir):
                        print(menu2)
                        consolesay("¿Por cual deseas empezar estas dentro de ejemplos?")
                        time.sleep(0.5)
                        respuesta = enviar_voz()
                        print("Tu respuesta " + respuesta)
                        #menu2 = "\n1) Cronograma instruccion añadir (ADD)\n2) Ejecucion de la instruccion SW \n3) Ejecucion de la instruccion JWZ"
                        #menuadd = "\n1) Fase de Busqueda \n2) Fase de busqueda de operandos\n3)Fase de ejecucion y almacenamiento del resultado"
                        if respuesta == "cronograma instrucción agregar":
                            texto_a_audio(datos['add'])
                            while(not salir):
                                consolesay(menuadd)
                                consolesay("¿Por cual deseas empezar?")
                                time.sleep(0.5)
                                respuesta = enviar_voz()
                                print("Tu respuesta " + respuesta)
                                if respuesta == "fase de búsqueda":
                                    ejecutar("busqueda")
                                elif respuesta == "fase de búsqueda de operandos":
                                    texto_a_audio(datos["operandos"])
                                elif respuesta == "fase de ejecución y almacenamiento del resultado":
                                    texto_a_audio(datos["ejecalmc"])
                                else:
                                    not_recognized()
                                    continue

                                if still():
                                    continue
                                else:
                                    break
                            # Para repetir el ciclo del "menu2"
                            continue

                        elif respuesta == "ejecución de la instrucción sw":
                            ejecutar("sw")
                        elif respuesta == "ejecución de la instrucción jwz": 
                            ejecutar("jwz")
                        else:
                            not_recognized()
                            continue

                        if still():
                            continue
                        else:
                            break
                    # Para repetir el ciclo de "opciones"
                    continue

                else:
                    not_recognized()
                    continue
                
                if still():
                    continue
                else:
                    break            
            # Para repetir el menu de aprendizaje, test, juegos
            continue

        ###### PARTE 2 - TEST ######  
        elif respuesta == "test":
            consolesay("Elegiste la opción TEST.")
            consolesay("En esta opción tienes para elegir en dar una prueba de entrada sobre PENSAMIENTO COMPUTACIONAL, o dar un examen sobre "+tema+".")
            consolesay("¿Cuál eliges?")
            texto_a_audio("¿Prueba de entrada Pensamiento Computacional? o ¿Examen - Ejecución de instrucciones?")
            
            while(not salir):
                print("\n 1) Prueba de entrada - Pensamiento Computacional\n 2) Ejecución de instrucciones\n") #Menu de Test (Por trabajar)
                consolesay("¿Por cual deseas empezar?")
                time.sleep(0.5)
                #COMPRUEBA QUE EL MENSAJE ENVIADO SEA VALIDO    
                respuesta = enviar_voz()
                print("Tu respuesta " + respuesta)
                if respuesta == "prueba de entrada pensamiento computacional":
                    consolesay("Escogiste: Prueba de entrada de Pensamiento Computacional")
                    consolesay("Empezemos con la prueba:")
                    print("------------------------------------------------------------------------------------")
                    texto_a_audio(datos['PE PREGUNTA 01'])
                    print("PRIMERA PREGUNTA: 1. ¿Cuál es el objetivo principal del pensamiento computacional?")
                    print("     \na) Resolver problemas utilizando algoritmos y abstracción.     \nb) Programar robots y sistemas autónomos.     \nc) Diseñar hardware de computadoras.\n")
                    consolesay("¿Cual es tu respuesta?")
                    texto_a_audio("¿a? ¿b? o ¿c?")
                    respuesta = enviar_voz()
                    print("Tu respuesta " + respuesta)
                    
                    if respuesta == "a":
                        consolesay("Tu respuesta es correcta. Muy bien.")
                        aumentarPuntos()
                    elif respuesta == "b" or respuesta =="c":
                        consolesay("Tu respuesta es incorrecta.")
                    else:
                        not_recognized()
                    time.sleep(0.5)
                    print("------------------------------------------------------------------------------------")
                    texto_a_audio(datos['PE PREGUNTA 02'])
                    print("SEGUNDA PREGUNTA: 2. El primer paso del pensamiento computacional es: identificar el problema.")
                    print("     \na) V     \nb) F\n")
                    consolesay("¿Cual es tu respuesta?")
                    respuesta = enviar_voz()
                    print("Tu respuesta " + respuesta)
                    if respuesta == "verdadero":
                        consolesay("Tu respuesta es correcta. Muy bien.")
                        aumentarPuntos()
                    elif respuesta == "falso":
                        consolesay("Tu respuesta es incorrecta.")
                    else:
                        not_recognized()
                    print("------------------------------------------------------------------------------------")
                        
                    pregunta = "¿Qué es un algoritmo en términos de pensamiento computacional?"
                        
                    texto_a_audio(datos['PE PREGUNTA 03'])
                    print("TERCERA PREGUNTA: ¿Qué es un algoritmo en términos de pensamiento computacional?")
                    alternativas = ["Un patrón de diseño visual","Un lenguaje de programación", "Una secuencia de pasos para resolver un problema", "Una representación gráfica de datos"]
                    respuesta_correcta ="Una secuencia de pasos para resolver un problema" # RESPUESTA CORRECTA
                    escribir_respuesta(pregunta, alternativas, respuesta_correcta)
                    if still():
                        continue
                    else:
                        break
                        
                elif respuesta == "ejecución de instrucciones":
                    print("------------------------------------------------------------------------------------")
                    consolesay("EJ PREGUNTA 01")
                    mostrar_pregunta(datos["EJ PREGUNTA 01"])
                    print("------------------------------------------------------------------------------------")
                    consolesay("EJ PREGUNTA 02")
                    mostrar_pregunta(datos["EJ PREGUNTA 02"])
                
                else:
                    not_recognized()
                    continue
                    
                if still():
                    continue
                else:
                    break
            # Para repetir el menu de aprendizaje, test, juegos
            continue

        ###### PARTE 3 - JUEGOS ######                
        elif respuesta == "juegos":
            consolesay("Elegiste la opción JUEGOS.")
            consolesay("El primer juego consta en contestar las preguntas, haciendo click en la imagen que crees que es la respuesta.")
            consolesay("En la fase de decodificacion del proceso de ejecucion de instrucciones de una computadora, ¿cual de estas imagenes representa el componente responsable de interpretar las instrucciones, determinar las operaciones a realizar y localizar los datos necesarios? Por favor, selecciona una de las siguientes imagenes.")
            class ComputerStructureQuizApp:
                def __init__(self, root):
                    self.root = root
                    self.root.title("JUEGO: EJECUCIÓN DE INSTRUCCIONES")
                    self.question_label = tk.Label(root, text="En la fase de decodificación del proceso de ejecución de instrucciones de una computadora, ¿cuál de estas imágenes representa el componente responsable de interpretar las instrucciones, determinar las operaciones a realizar y localizar los datos necesarios? Por favor, selecciona una de las siguientes imágenes.")
                    self.question_label.pack()
                    self.image_frame = tk.Frame(root)
                    self.image_frame.pack()
                    self.image_labels = []
                    for _ in range(4):
                        image_label = tk.Label(self.image_frame, image=None)
                        image_label.pack(side=tk.LEFT, padx=10)
                        image_label.bind("<Button-1>", self.check_answer)
                        self.image_labels.append(image_label)
                    self.correct_answer = 0  # Índice de la respuesta correcta
                    self.load_question()
                def load_question(self):
                    # Cargar la pregunta y las imágenes aquí
                    question = "En la fase de decodificación del proceso de ejecución de instrucciones de una computadora, ¿cuál de estas imágenes representa el componente responsable de interpretar las instrucciones, determinar las operaciones a realizar y localizar los datos necesarios? Por favor, selecciona una de las siguientes imágenes."
                    options = ["RAM", "GPU", "HDD", "CPU"]
                    self.question_label.config(text=question)
                    self.correct_answer = 3  # Respuesta correcta en la posición 0 (RAM)
                    for i in range(4):
                        image_path = f"option_{i+1}.png"
                        image = Image.open(f"imgs/{image_path}")
                        image = image.resize((200, 200))
                        photo = ImageTk.PhotoImage(image)
                        self.image_labels[i].config(image=photo)
                        self.image_labels[i].image = photo
                def check_answer(self, event):
                    clicked_label = event.widget
                    clicked_index = self.image_labels.index(clicked_label)
                    if clicked_index == self.correct_answer:
                        consolesay("¡Respuesta correcta!")
                        sys.exit(1)
                    else:
                        consolesay("Respuesta incorrecta.")
                    self.load_question()
            if __name__ == "__main__":
                root = tk.Tk()
                app = ComputerStructureQuizApp(root)
                
                root.mainloop()
        #SI EL MENSAJE ENVIADO NO ES ERRONEO LE PIDE AL USUARIO SELECCIONAR UNA OPCION VALIDA
        else:
            not_recognized()