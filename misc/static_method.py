def calculated_once_dict(func: callable) -> callable:
    """
    Runs a function once, saves it internally.
    From second run returns saved results from first run.
    :param func: Function to process
    :type func: callable
    :return: Function's call results from first run
    :rtype: callable
    """

    def wrapped(self, *args, **kwargs):
        function_result = self.__dict__.get("_" + func.__name__, None)
        if not function_result:
            function_result = func(self, *args, **kwargs)
            self.__dict__["_" + func.__name__] = function_result
        return function_result

    return wrapped
