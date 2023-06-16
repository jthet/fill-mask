#!/usr/bin/env python3

import sys, os
from transformers import pipeline

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


def unmasker_fun(input_sentence: str, num_results: int, model_name: str) -> list:
    '''
    Uses the pipeline function to apply the 'fill-mask' ML model from Hugging Face to a sentence

    Args:
        input_sentance (str):   The input sentance with the <mask> word in it. 
        num_results (int):      The number of returns (word predictions)

    Output:
        unmasked_results (list):    A list (of size num_results) of dictionaries containting the fill-mask output
    '''
    valid_model_name = True
    
    try:
        int(num_results)
    except Exception as e:
        return f'Error: {e}' +'\n'

    # Testing if given model name is valid, if not uses the base model
    # base model is "distilroberta-base"
    try:
        unmasker = pipeline('fill-mask', model=str(model_name))
    except Exception as e:
        print(f'Error: {e}\n\n{model_name} is an invalid model name. Instead, the "distilroberta-base" was used')
        valid_model_name = False
        unmasker = pipeline('fill-mask', model='distilroberta-base')

    try:
        unmasked_results = unmasker(input_sentence, top_k = int(num_results))
    except Exception as e:
        return str(e)+'\n' 

    return unmasked_results, valid_model_name


def main():

    # destination for output file
    directory = "fill-mask-output"
    filename = os.path.join(directory, "output.txt")
    model_name = 'distilroberta-base'
    model_str = ''

    # Confirming proper inputs
    try:
        input_string = sys.argv[1]
        num_results = sys.argv[2]
    except Exception as e:
        write_to_file(f'{e}\nNeed proper CLI inputs: <input_string> and <num_results> (and optionally) <model_name>\n', filename)
        return
    
    # Taking in optional input 'model_name', defualt is 'dsitilroberta-base'
    if len(sys.argv) == 4:
        model_name = sys.argv[3]



    # running fill-mask on inputs
    try:
        (unmasked_output, valid_model_name) = unmasker_fun(input_string, num_results, model_name)
    except Exception as e:
        write_to_file(f'{e}\nNeed proper CLI inputs: <input_string> and <num_results> (and optionally) <model_name>\n', filename)
        return

    if valid_model_name == False:
        model_str = f'Error: {model_name} is an invalid model name. Instead, the "distilroberta-base" was used\n'
    else:
        model_str = f'Using model: {model_name}\n'

    # writing output to file
    if type(unmasked_output) == list:
        output_string = ""
        for result in unmasked_output: 
            output_string += str(result) + '\n'
    else:
        output_string = str(unmasked_output)
    
    write_to_file(model_str + output_string, filename)

    print('\n'+("*"*25)+' Content of "/fill-mask-output/output.txt" '+("*"*25)+'\n')
    with open(filename, 'r') as file:
            print(file.read())



if __name__ == "__main__":
    main()