from .base_validator import BaseValidator

class SaleValidator(BaseValidator):
    
    def __init__(self):
        super(SaleValidator,self).__init__()

    #return status, error message
    #status: true -> validation is succesfull
    #status: false -> error occurs
    @staticmethod
    def validate_add(request):
        try:
            BaseValidator.word_in_range(request,"sale_code",1,6, "Sale Code")
            #BaseValidator.word_in_range(request,'sale_start_at',1,6, "Sale Start")
            #BaseValidator.word_in_range(request,'sale_finish_at',5,50, "Sale Finish")
            BaseValidator.word_in_range(request,'description',5,15, "Sale Description")
            BaseValidator.word_in_range(request,'sale_price',0,10, "Sale Price")
            return True,""
        except Exception as e:
            return False,str(e)
        