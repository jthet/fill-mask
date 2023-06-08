#!/usr/bin/env python3

import sys, os
from transformers import pipeline


def unmasker_fun(input_sentence: str, num_results: int) -> list:
    '''
    Uses the pipeline function to apply the 'fill-mask' ML model from Hugging Face to a sentence

    Args:
        input_sentance (str):   The input sentance with the <mask> word in it. 
        num_results (int):      The number of returns (word predictions)

    Output:
        unmasked_results (list):    A list (of size num_results) of dictionaries containting the fill-mask output
    '''
    
    try:
        int(num_results)
    except Exception as e:
        return f'Error: {e}'

    unmasker = pipeline('fill-mask', model='distilroberta-base')

    try:
        unmasked_results = unmasker(input_sentence, top_k = int(num_results))
    except Exception as e:
        return e

    return unmasked_results

def write_to_file(output_string, filename):
    '''
    Writes a string into a file

    Args:
        input_string:   The string to be written to a file
        filename:       The destiantion file path for the string

    Returns:
        None
    '''

    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            file.write(output_string)
        print("Output written to", filename)
    except IOError:
        print("Error writing to file", filename)

def main():

    # destination for output file
    directory = "TapisOutput"
    filename = os.path.join(directory, "output.txt")

    # Confirming proper inputs
    try:
        input_string = sys.argv[1]
        num_results = sys.argv[2]
    except Exception as e:
        write_to_file(f'{e}\nNeed proper CLI inputs: <input_string> and <num_results>\n', filename)
        return

    # running fill-mask on inputs
    unmasked_output = unmasker_fun(input_string, num_results)

    # writing output to file
    if type(unmasked_output) == list:
        output_string = ""
        for result in unmasker_fun(input_string, num_results):
            output_string += str(result) + '\n'
    else:
        output_string = str(unmasker_fun(input_string, num_results)) + '\n'
    
    write_to_file(output_string, filename)

    with open(filename, 'r') as file:
            print(file.read())



if __name__ == "__main__":
    main()