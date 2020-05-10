class Response(object):
    def success(self, data=[]):
        return {'code': 200, 'msg': '成功！', 'data': data}

    def failed(self, msg=''):
        return {'code': 500, 'msg': '失败！错误信息：' + str(msg) + '，请联系管理员。'}
