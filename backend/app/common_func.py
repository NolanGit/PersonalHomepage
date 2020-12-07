import redis
import random
import hashlib
import inspect


class CommonFunc(object):

    def random_str(self, num):
        H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

        salt = ''
        for i in range(num):
            salt += random.choice(H)

        return salt

    def md5_it(self, str):
        str_md5 = hashlib.md5(str.encode('utf-8')).hexdigest()
        return str_md5

    def dict_list_get_single_element(self, list, key, value, target_key, index=0):
        '''
            获取字典列表中第一个key==value的target_key的值，index的传入可以加速
        '''
        # 不知道index情况下遍历
        result = None
        if index == 0:
            for single_element in list:
                if single_element[key] == value:
                    result = single_element[target_key]
                    break
        # 知道index情况下加速结果返回速度
        else:
            temp = True
            try:
                temp = list[index][key] == value
            except:
                temp = False
            if temp:
                result = list[index][target_key]
            else:
                for single_element in list:
                    if single_element[key] == value:
                        result = single_element[target_key]
                        break
        return result

    def dict_list_get_all_element(self, list, key, value, target_key):
        '''
            获取字典列表中全部的key==value的target_key的值，返回一个列表
        '''
        result = []
        for single_element in list:
            if single_element[key] == value:
                result.append(single_element[target_key])
            else:
                pass
        return result

    def is_data_existed_in_db(self, db_class, key, target):
        status = db_class.select().where(key == target).dicts()
        return True if len(status) != 0 else False

    def attr_to_dict(self, instance):
        aaa = inspect.getmembers(instance, lambda a: not (inspect.isroutine(a)))
        bbb = [a for a in aaa if not (a[0].startswith('__') and a[0].endswith('__'))]
        ccc = {}
        for b in bbb:
            ccc[b[0]] = b[1]
        return ccc


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper