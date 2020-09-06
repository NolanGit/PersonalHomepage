from flask import jsonify


class Check(object):

    def __init__(self, check_target):
        self.check_target = check_target

    def check_failed(self):
        return jsonify({'code': 400, 'msg': '非法的参数！'})

    def not_none(self):
        if self.check_target != None:
            return self
        else:
            return self.check_failed()

    def not_empty(self):
        flag = False

        if isinstance(self.check_target, str):
            if self.check_target != None:
                flag = True
            else:
                flag = False

        if isinstance(self.check_target, list):
            if self.check_target != []:
                flag = True
            else:
                flag = False

        if flag:
            return self
        else:
            return self.check_failed()
