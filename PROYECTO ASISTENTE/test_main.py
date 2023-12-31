import json
from pathlib import Path
from PIL import Image
from utils_audio import console_print_say
from utils_audio import console_print_say_options
from utils_audio import recognize_voice

# Get paths
current_path = Path.cwd()
database_path = Path("info.json")
# Global variables
username = "Usuario"
info_dictionary = {}
commands = {
    "continuar": "Continuar",
    "regresar": "Regresar",
    "regresar al inicio": "Regresar al inicio",
    "salir": "Salir"
}
options = {
    "uno": 0,
    "dos": 1,
    "tres": 2,
    "cuatro": 3,
    "cinco": 4,
}

with open("info.json", 'r', encoding="utf-8") as file:
    info_dictionary = json.load(file)

# Methods
def get_key_list_if_exists(current_structure):
    try:
        return list(current_structure.keys())
    except KeyError:
        not_recognized()
        return None
    
def last_menu(queries):
    queries_stack = queries.copy()
    queries_stack.reverse()
    current_structure = info_dictionary
    while queries_stack != []:
        query = queries_stack.pop()
        current_structure = current_structure[query]
    
    return current_structure

def show_question(question_key):
    print("------------------------------------------------------------------------------------")
    print(question_key)
    question_structure = info_dictionary["Preguntas"][question_key]
    console_print_say(question_structure["pregunta"][0])
    questions = list(question_structure["alternativas"].keys())

    for i, alternativa in enumerate(questions, start = 1):
        print(f"{str(i)}) {alternativa}")
    user_answer = recognize_voice()
    
    if is_right_answer(question_structure, user_answer):
        console_print_say("¡Respuesta correcta!")
        # upScore()
    else:
        console_print_say("Respuesta incorrecta")

def is_right_answer(question, response):
    if question["respuesta"][0].lower() == response.lower():
        return True
    
    alternative_exists = exists_in_dictionary(question, response)
    if alternative_exists:
        return bool(question["alternativas"][response])

    alternative_index = exists_in_dictionary(options, response)
    if not alternative_index:
       return False
    
    print("Revisaremos numéricamente")
    alternative = list(question["alternativas"].keys())[alternative_index]
    return bool(question["alternativas"][alternative])

def exists_in_dictionary(current_structure, query):
    if not is_dictionary(current_structure):
        return None
    try:
        return current_structure[query]
    except KeyError:
        return None

def is_dictionary(current_structure):
    if type(current_structure) is dict:
        return True
    else:
        return False

def not_recognized():
    console_print_say(username + " creo que no has respondido con alguna opción posible a elegir en este contexto")
    return False

def in_question_section(queries):
    if not queries:
        return False
    
    return queries[-1] == "Preguntas"

def left_questions(current_structure, iterator):
    if not is_dictionary(current_structure):
        print("No es")
        return False
    return len(list(current_structure.keys())) >= iterator

def pop_if_is_possible(queries):
    if queries:
        queries.pop()

def show_existent_images(queries):
    queries_stack = queries.copy()
    queries_stack.reverse()
    queries_stack.pop()
    queries_stack.append("imágenes".capitalize())
    image_paths = info_dictionary
    
    while queries_stack != []:
        temp_query = queries_stack.pop()
        image_paths = image_paths[temp_query]

    for path in image_paths:
        img = Image.open(f"imgs/{path}")
        img.show()

if __name__ == "__main__":
    console_print_say(info_dictionary["Bienvenida"])
    username = recognize_voice()
    print()
    current_structure = info_dictionary
    queries = []
    iterator = 1
    while True:
        if in_question_section(queries) and left_questions(current_structure, iterator):
            show_question("EJ PREGUNTA " + str(iterator))
            iterator = iterator + 1
            continue
        elif in_question_section(queries):
            pop_if_is_possible(queries)
            current_structure = last_menu(queries)
        
        print()

        if is_dictionary(current_structure):
            console_print_say("\nElige que deseas conocer")
            interaction = get_key_list_if_exists(current_structure)
            console_print_say_options(interaction)
        else:
            interaction = current_structure
            console_print_say(interaction)
        
        print()

        if not is_dictionary(current_structure):
            show_existent_images(queries)
            pop_if_is_possible(queries)
            console_print_say("\n¿Quieres seguir aprendiendo?")
            console_print_say(list(commands.values()))
        
        query = recognize_voice()
        query = query.capitalize()
        pre_structure = None
        
        if query == "continuar".capitalize():
            current_structure = last_menu(queries)
        elif query == "regresar".capitalize():
            pop_if_is_possible(queries)
            current_structure = last_menu(queries)
        elif query == "regresar al inicio".capitalize():
            queries = []
            current_structure = info_dictionary
        elif query == "salir".capitalize():
            exit(0)
        else:
            pre_structure = exists_in_dictionary(current_structure, query)
        
        if pre_structure:
            current_structure = pre_structure
            queries.append(query)
        elif not is_dictionary(current_structure):
            console_print_say("No es una opción válida, se retornará a un menú cercano")
            current_structure = last_menu(queries)
        else:
            not_recognized()
            
        if queries:
            console_print_say(f"Elegiste la opción {query.upper()}")
        
