import time, json, copy

from flask_sqlalchemy import SQLAlchemy
from edustack import wsgiApp

db = SQLAlchemy(wsgiApp)

def isJsonable(obj):
    try:
        json.dumps(obj)
    except:
        return False
    else:
        return True

def toJsonTime(timeField):
    return time.mktime(timeField.timetuple())

def toDictExt(*attrs):
    def wrapper(model):
        return {k:v for k,v in toDict(model).items() if k in attrs}
    return wrapper

def toDict(model):
    if not hasattr(model, "__dict__"):
        return {}
    retDict = {k:v for k,v in model.__dict__.items() if isJsonable(v)}
    jsonDict = getattr(model, "_jsonMapDict", {})
    for (key,fun) in jsonDict.items():
        if hasattr(model, key):
            field = getattr(model, key)
            retDict[key] = fun(field)
    return retDict

class FieldMixin(object):
    _jsonMapDict = {
        'created_at': toJsonTime,
        'user': toDictExt('name', 'email', 'created_at', 'admin', 'image'),
        }

    _RE_EMAIL = r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$'
    _RE_MD5 = r'^[0-9a-f]{32}$'
    _regexMapDict = {
        'email' : _RE_EMAIL,
        'password': _RE_MD5,
        }

class Page(object):
    def __init__(self, item_count, page_index=1, page_size=10):
        '''
        Init Pagination by item_count, page_index and page_size.

        >>> p1 = Page(100, 1)
        >>> p1.page_count
        10
        >>> p1.offset
        0
        >>> p1.limit
        10
        >>> p2 = Page(90, 9, 10)
        >>> p2.page_count
        9
        >>> p2.offset
        80
        >>> p2.limit
        10
        >>> p3 = Page(91, 10, 10)
        >>> p3.page_count
        10
        >>> p3.offset
        90
        >>> p3.limit
        10
        '''
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        if (item_count == 0) or (page_index < 1) or (page_index > self.page_count):
            self.offset = 0
            self.limit = page_size
            self.page_index = 1
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__

    def toDict(self):
        return {
            'page_index': self.page_index,
            'page_count': self.page_count,
            'item_count': self.item_count,
            'has_next': self.has_next,
            'has_previous': self.has_previous
        }

def get_items_by_page(pageIndex, Model):
    total = Model.query.count()
    page = Page(total, pageIndex)
    models = Model.query.offset(page.offset).limit(page.limit)
    return models, page

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)