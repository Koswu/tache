import fakeredis

from tache import RedisCache


def test_cached():
    r = fakeredis.FakeStrictRedis()
    r.flushall()
    cache = RedisCache(conn=r)

    @cache.cached()
    def func(id):
        if hasattr(func, 'called'):
            return {'new': 1, 'old': 2}
        func.called = True
        return {'old': 1}

    k = func(33)
    assert k['old'] == 1
    k = func(33)
    assert k['old'] == 1
    assert k['new'] == 1
    assert k['old'] == 2


def test_batch():
    r = fakeredis.FakeStrictRedis()
    r.flushall()
    cache = RedisCache(conn=r)

    class Cls:
        def __init__(self):
            self.called = False

        @cache.batch()
        def func(self, *ids):
            if hasattr(self, 'called') and getattr(self, 'called'):
                return [{'new': id_ * 2} for id_ in ids]
            self.called = True
            return [{'old': id_} for id_ in ids]

    c = Cls()
    res_li = c.func(1, 2)
    a = res_li[0]
    assert a['old'] == 1
    assert a['new'] == 2


def test_batch_classmethod():
    r = fakeredis.FakeStrictRedis()
    r.flushall()
    cache = RedisCache(conn=r)

    class OldClass:
        def __init__(self, val):
            self.old = val

    class NewClass:
        def __init__(self, val):
            self.new = val * 2

    class Cls:
        def __init__(self):
            self.called = False

        @cache.batch()
        @classmethod
        def func(cls, *ids):
            if hasattr(cls, 'called') and getattr(cls, 'called'):
                return [NewClass(id_) for id_ in ids]
            cls.called = True
            return [OldClass(id_) for id_ in ids]

    res_li = Cls.func(1, 2)
    a = res_li[0]
    assert a.old == 1
    assert a.new == 2
