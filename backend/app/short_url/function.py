import time
import datetime
from peewee import DoesNotExist
from ..model.short_content_model import short_content as short_content_table

DICT = {
    0: '1',1: '2',2: '3',3: '4',4: '5',5: '6',6: '7',7: '8',8: '9',9: 'a',10: 'b',11: 'c',12: 'd',13: 'e',14: 'f',15: 'g',16: 'h',17: 'i',18: 'j',19: 'k',20: 'm',21: 'n',22: 'o',23: 'p',24: 'q',25: 'r',26: 's',27: 't',28: 'u',29: 'v',30: 'w',31: 'x',32: 'y',33: 'z',34: 'A',35: 'B',36: 'C',37: 'D',38: 'E',39: 'F',40: 'G',41: 'H',42: 'J',43: 'K',44: 'L',45: 'M',46: 'N',47: 'P',48: 'Q',49: 'R',50: 'S',51: 'T',52: 'U',53: 'V',54: 'W',55: 'X',56: 'Y',57: 'Z',
}

DICT_DISORDER = {
    0: 'B',1: 'H',2: 'q',3: 'D',4: 'b',5: 'j',6: 'Q',7: 'z',8: '6',9: 'x',10: 'L',11: 'R',12: 'P',13: 'Z',14: 'n',15: 'v',16: 'e',17: '9',18: 'M',19: '3',20: 'W',21: '5',22: 'G',23: 'V',24: 'r',25: 'h',26: 'k',27: 'c',28: 'E',29: 'g',30: 'C',31: 'd',32: 'T',33: '7',34: 'K',35: 'm',36: 'i',37: 'S',38: 'f',39: 'J',40: 'U',41: 'Y',42: 'F',43: 'u',44: '1',45: '4',46: 'y',47: 'o',48: 'w',49: '2',50: 'a',51: '8',52: 'A',53: 'p',54: 'N',55: 's',56: 't',57: 'X'
}


def base_58(target: int):
    # 接受一个整数，返回不会重复的较短的字符串
    r = ''
    target = int(str(target) + str(time.time()).split('.')[0][-6:])
    while target > 58:
        r += str(DICT_DISORDER[target % 58])
        target = target // 58
    r += str(DICT_DISORDER[target])
    return r[::-1]


def set_content(content, type, expire_time=None):
    default_expire_time = datetime.datetime.now() + datetime.timedelta(weeks=100 * 52)  # 有效期覆盖社会主义初级阶段
    s = short_content_table(code='', content='', type='', is_valid=1, expire_time=default_expire_time if expire_time == None else expire_time, update_time=datetime.datetime.now()).save()
    _id = s.id
    _code = base_58(_id)
    short_content_table.update(code=_code).where(short_content_table.id == _id).execute()


def get_content(code):
    try:
        _ = short_content_table.get(short_content_table.code == code)
        return {'type': _.type, 'content': _.content}
    except DoesNotExist:
        return None