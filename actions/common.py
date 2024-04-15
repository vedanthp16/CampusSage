from fuzzywuzzy import process

def CorrectSpelling(input_string,possible_values):
    match = process.extractOne(input_string,possible_values)
    if match and match[1] > 80:
        return match[0]
    else:
        return input_string