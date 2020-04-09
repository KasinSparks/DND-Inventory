class FileNotSuppliedException(Exception):
    def __init__(self): 
        self.value = "No file was supplied." 
  
    # __str__ is to print() the value 
    def __str__(self): 
        return(repr(self.value)) 