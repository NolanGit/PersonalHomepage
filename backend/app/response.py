from flask import jsonify


class Response(object):

    def success(self, data=[]):
        return jsonify({'code': 200, 'msg': '成功！', 'data': data})

    def failed(self, msg=''):
        return jsonify({'code': 500, 'msg': '失败！错误信息：' + str(msg) + '，请联系管理员。'})

    def refuse(self, msg=''):
        return jsonify({'code': 403, 'msg': '失败！没有权限进行此操作。' + str(msg)})
