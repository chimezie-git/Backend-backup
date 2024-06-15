class CustomResponse:
    def __init__(self, code:int, data:dict, has_error:bool, message:str="") -> None:
        self.code = code
        self.data = data
        self.__has_error = has_error
        self.message = message
    def has_error(self):
        return self.__has_error


