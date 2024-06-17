class CustomResponse:
    def __init__(self, code:int, data:dict, has_error:bool) -> None:
        self.code = code
        self.data = data
        self.__has_error = has_error
    def is_success(self):
        return (self.code == 200 or self.code ==201) and (not self.__has_error)
    def has_error(self):
        return self.__has_error


