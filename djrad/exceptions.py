class APIException(Exception):
    def __init__(self, message, status=400, error_code=0):
        super(Exception, self).__init__()
        self.message = message
        self.status = status
        self.error_code = error_code


class APIValidationException(Exception):
    def __init__(self, error, status=400, error_code=0):
        super(Exception, self).__init__()
        self.error = error
        self.status = status
        self.error_code = error_code
