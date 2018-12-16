from .base_validator import BaseValidator

class TerminalValidator(BaseValidator):
    
    def __init__(self):
        super(TerminalValidator,self).__init__()

    #return status, error message
    #status: true -> validation is succesfull
    #status: false -> error occurs
    @staticmethod
    def validate_add(request):
        try:
            BaseValidator.word_in_range(request,"terminal_name",4,50, "Terminal Name")
            BaseValidator.word_in_range(request,'terminal_code',1,6, "Terminal Code")
            BaseValidator.word_in_range(request,'e_mail',5,50, "Terminal Email")
            BaseValidator.word_in_range(request,'phone',5,15, "Terminal Phone")
            BaseValidator.word_in_range(request,'address',5,250, "Terminal Address")
            BaseValidator.word_in_range(request,'description',5,60, "Terminal Description")
            BaseValidator.word_in_range(request,'city',0,15, "Terminal City")
            return True,""
        except Exception as e:
            return False,str(e)
        