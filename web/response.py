class Response():
    def __init__(self, code, message, data):
        self._code = code
        self._message = message
        self._data = data

    def success(self, data=''):
        self._code = 200
        self._message = '成功'
        self._data = data

    def failure(self, data=''):
        self._code = 1000
        self._message = '失败'
        self._data = data

    @property
    def data(self):
        body = self.__dict__
        body["code"] = body.pop("_code")
        body["message"] = body.pop("_message")
        body["data"] = body.pop("_data")
        return body
