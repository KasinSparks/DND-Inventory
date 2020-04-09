def shorten_string(string : str, max_length : int):
    shortened_name = string

    if len(string) > max_length:
        shortened_name = string[0:max_length] + '...'
    
    return shortened_name