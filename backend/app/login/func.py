import random
import hashlib

class CommonFunc(object):

    def random_str(self,num):
        H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

        salt = ''
        for i in range(num):
            salt += random.choice(H)

        return salt

    def md5_it(self,str):
        str_md5 = hashlib.md5(str.encode('utf-8')).hexdigest()
        return str_md5
