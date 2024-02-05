def map_number(input: int, input_min: int, input_max: int, output_min: int, output_max: int):
    return output_min + ((output_max - output_min) / (input_max - input_min)) * (input - input_min);