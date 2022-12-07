
class RespSuccessData:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

class RespErrorData:
    def __init__(self, status, message):
        self.status = status
        self.message = message
