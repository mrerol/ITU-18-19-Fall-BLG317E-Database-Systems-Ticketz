from .base_validator import BaseValidator

class UserValidator(BaseValidator):
    
    def __init__(self):
        super(UserValidator,self).__init__()

    #return status, error message
    #status: true -> validation is succesfull
    #status: false -> error occurs
    @staticmethod
    def validate_add(request):
        try:
            BaseValidator.word_in_range(request,"user_name",1,15, "User Name")
            BaseValidator.word_in_range(request,'email',5,50, "Email")
            BaseValidator.word_in_range(request,'password',5,50, "Password")
            BaseValidator.word_in_range(request,'name',5,50, "Name")
            BaseValidator.word_in_range(request,'surname',5,50, "Surname")
            BaseValidator.word_in_range(request,'phone',5,50, "Phone")
            BaseValidator.word_in_range(request,'address',5,250, "Address")
            return True,""
        except Exception as e:
            return False,str(e)
        