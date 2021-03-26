def static(func):
    def wrapped(self, *args, **kwargs):
        dict_val = self.__dict__.get("_" + func.__name__, None)
        if not dict_val:
            dict_val = func(self, *args, **kwargs)
            self.__dict__["_" + func.__name__] = dict_val
        return dict_val

    return wrapped
