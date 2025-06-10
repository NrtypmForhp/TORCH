# [= Main functions for TORCH =]

import os, json

# [= Replace commas for javascript =]
# Directly connected to restore_commas function in static/main_scripts.js
def replace_commas(string:str) -> str:
    new_string = string.replace("'", "@single_quote@").replace('"', "@double_quote@")
    return new_string

# [= Replace dict strings recursively =]
def replace_strings_recursive(dictionary:dict, replacement_func:callable) -> dict:
    new_dictionary = {}
    for key, value in dictionary.items(): # Loop trought dict
        if isinstance(value, str): # Check if the value is a string
            new_dictionary[key] = replacement_func(value) # Set modified value to new dict
        elif isinstance(value, dict): # If the value is a dict
            new_dictionary[key] = replace_strings_recursive(value, replacement_func) # Repeat function recursive to the nested dictionary
        elif isinstance(value, list): # If the value is a list
            new_dictionary[key] = [
                replace_strings_recursive(item, replacement_func)
                if isinstance(item, dict) else
                replacement_func(item) if isinstance(item, str) else item
                for item in value
            ] # Replace all items in a list and do it recursively if it's a dict
        else:
            new_dictionary[key] = value # Leave original value if is not one of recognized instance
    return new_dictionary

# [= Load and read languages files =]
def load_languages_files(languages_directory:str) -> dict:
    # Set language dict
    language = {}
    
    # Get languages files names
    languages_files_list = os.listdir(languages_directory)
    
    # Loop files
    for language_file in languages_files_list:
        lang = language_file[:language_file.index("_")] # Get language (example: EN or IT)
        file = language_file[language_file.index("_") + 1:language_file.index(".txt")] # Get file (example: main or home)
        
        # Create language key if not exists
        try: language[lang]
        except KeyError: language[lang] = {}
        
        # Create file key if not exists
        try: language[lang][file]
        except KeyError: language[lang][file] = {}
        
        # Open .txt language file
        with open(os.path.join(languages_directory, language_file), "r", encoding="utf-8") as opened_language_file:
            # Loop file lines
            for text in opened_language_file:
                try:
                    text_parts = text.split(":", 1) # Split text into 2 parts, first for the dictionary key and second for text
                    language[lang][file][text_parts[0].strip()] = text_parts[1].strip() # Set language dictionary key
                except:
                    print(f"!! Warning !! Error on file: {language_file} - Exception at text: {text}")
                    pass
    
    return language

# [= Get language dictionary for javascript =]
def get_language_dict(language:str, language_dict:dict) -> dict:
    new_language_dict = language_dict[language]
    new_language_dict = replace_strings_recursive(new_language_dict, replace_commas)
    return {"response": "ok", "language": json.dumps(new_language_dict)}