import time, uuid

def tryParse(obj, cls, default):
    try:
        return cls(obj)
    except:
        return default

def next_id(t=None):
    if t is None:
        t = time.time()
    return '%015d%s000' % (int(t*1000), uuid.uuid4().hex)