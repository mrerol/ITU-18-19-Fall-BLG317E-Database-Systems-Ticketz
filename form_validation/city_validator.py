from .base_validator import BaseValidator

class CityValidator(BaseValidator):
    
    def __init__(self):
        super(CityValidator,self).__init__()

    #return status, error message
    #status: true -> validation is succesfull
    #status: false -> error occurs
    @staticmethod
    def validate_add(request):
        try:
            BaseValidator.word_in_range(request,'city_code' ,0,3, "City Code")
            BaseValidator.word_in_range(request,'city_name',3,25, "City Name")
            #BaseValidator.word_in_range(request,'population',10,100000000, "Population")
            BaseValidator.word_in_range(request,'region',5,50, "Region")
            #BaseValidator.word_in_range(request,'altitude',10,10000, "Altitude")
            return True,""
        except Exception as e:
            return False,str(e)
        