class EmptyQueryException(Exception):
    def __init__(self): 
        self.value = "The query string was either None or empty..." 
  
    # __str__ is to print() the value 
    def __str__(self): 
        return(repr(self.value)) 