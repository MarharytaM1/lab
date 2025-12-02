# initial_i_checker.py

import re

EXCEPTIONS = {"иноді", "иний", "ирій", "икати", "инший"}

def find_initial_i_errors(text):
    
    pattern = r"\b[Ии][А-Яа-яіїєґ'’\d-]*" 
    
    highlights = []
    last_index = 0
    
    for match in re.finditer(pattern, text):
        word = match.group()
        start, end = match.start(), match.end()
        
        # ... (решта логіки залишається без змін) ...
        if start > last_index:
            highlights.append((text[last_index:start], None))
            
        if word.lower() not in EXCEPTIONS:
            highlights.append((word, "початкове-и"))
        else:
            highlights.append((word, None))
            
        last_index = end

    if last_index < len(text):
        highlights.append((text[last_index:], None))

    return highlights