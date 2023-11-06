import json
from pathlib import Path
from utils_audio import console_print_say
from utils_audio import recognize_voice


# Get paths
current_path = Path.cwd()
database_path = Path("info.json")
# Global variables
username = "Usuario"
info_dictionary = {}
commands = {
    "continuar": "continuar",
    "regresar": "regresar",
    "salir": "salir"
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

def exists_in_dictionary(current_structure, query):
    try:
        return current_structure[query]
    except KeyError:
        not_recognized()
        return None


def is_dictionary(current_structure):
    if type(current_structure) is dict:
        return True
    else:
        return False

def not_recognized():
    console_print_say(username + " creo que no has respondido con alguna de las instrucciones indicadas anteriormente")
    console_print_say("Responde con una de las alternativas mencionadas.")
    return False

if __name__ == "__main__":
    console_print_say(info_dictionary["bienvenida"])
    username = recognize_voice()
    current_structure = info_dictionary
    queries = []
    while True:
        if is_dictionary(current_structure):
            interaction = get_key_list_if_exists(current_structure)
            print("is dictionary")
        else:
            interaction = current_structure

        console_print_say(interaction)

        if not is_dictionary(current_structure):
            if queries:
                queries.pop()
            console_print_say(get_key_list_if_exists(commands))
        
        query = recognize_voice()
        pre_structure = None
        
        if query == "continuar":
            current_structure = last_menu(queries)
        elif query == "regresar":
            if queries:
                queries.pop()
            current_structure = last_menu(queries)
        elif query == "regresar al inicio":
            queries = []
            current_structure = info_dictionary
        elif query == "salir":
            exit(0)
        else:
            pre_structure = exists_in_dictionary(current_structure, query)
        
        if pre_structure:
            current_structure = pre_structure
            queries.append(query)
        
        print("Ciclo terminado")
        print(queries)

        