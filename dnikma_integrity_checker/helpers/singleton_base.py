class Singleton:

    def __init__(self, cls):
        self._cls = cls

    def Instance(self, conn_kwargs: dict = None):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls(conn_kwargs)
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through the `Instance()` function.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)
