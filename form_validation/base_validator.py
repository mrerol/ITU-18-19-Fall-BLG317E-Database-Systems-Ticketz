class BaseValidator():
    
    def __init__(self):
        pass

    @staticmethod
    def word_in_range(req,key,minl,maxl,str_key):
        if key not in req.form:
            raise Exception(str(str_key) + " is not found in request")
        elif len(req.form[key]) <= minl or  len(req.form[key]) >= maxl:
            raise Exception( str(str_key) + " is not in range")
            