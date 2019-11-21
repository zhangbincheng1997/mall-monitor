class Response:
    @staticmethod
    def status(code, message, data):
        return {'code': code, 'message': message, 'data': data}

    @staticmethod
    def success(message='成功', data=''):
        return {'code': 200, 'message': message, 'data': data}

    @staticmethod
    def failure(message='失败', data=''):
        return {'code': 1000, 'message': message, 'data': data}
