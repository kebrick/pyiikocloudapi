import functools
import inspect
import warnings

string_types = (type(b''), type(u''))


def deprecated(reason):
    if isinstance(reason, string_types):
        def decorator(func1):

            if inspect.isclass(func1):
                fmt1 = "Вызов эксперементального класаs {name} ({reason})."
            else:
                fmt1 = "Вызов эксперементальной функции {name} ({reason})."

            @functools.wraps(func1)
            def new_func1(*args, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(
                    fmt1.format(name=func1.__name__, reason=reason),
                    category=DeprecationWarning,
                    stacklevel=2
                )
                warnings.simplefilter('default', DeprecationWarning)
                return func1(*args, **kwargs)

            return new_func1

        return decorator

    elif inspect.isclass(reason) or inspect.isfunction(reason):
        func2 = reason

        if inspect.isclass(func2):
            fmt2 = "Вызов эксперементального класа {name}."
        else:
            fmt2 = "Вызов эксперементальной функции {name}."

        @functools.wraps(func2)
        def new_func2(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                fmt2.format(name=func2.__name__),
                category=DeprecationWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', DeprecationWarning)
            return func2(*args, **kwargs)

        return new_func2

    else:
        raise TypeError(repr(type(reason)))



class ExperimentalWarning(Warning):
    pass

def experimental(reason):
    if isinstance(reason, string_types):
        def decorator(func1):

            if inspect.isclass(func1):
                fmt1 = "Вызов эксперементального класа {name}, {reason}."
            else:
                fmt1 = "Вызов эксперементальной функции {name}, {reason}."

            @functools.wraps(func1)
            def new_func1(*args, **kwargs):
                warnings.simplefilter('always', ExperimentalWarning)
                warnings.warn(
                    fmt1.format(name=func1.__name__, reason=reason),
                    category=ExperimentalWarning,
                    stacklevel=2
                )
                warnings.simplefilter('default', ExperimentalWarning)
                return func1(*args, **kwargs)

            return new_func1

        return decorator

    elif inspect.isclass(reason) or inspect.isfunction(reason):
        func2 = reason

        if inspect.isclass(func2):
            fmt2 = "Вызов эксперементального класа {name}."
        else:
            fmt2 = "Вызов эксперементальной функции {name}."

        @functools.wraps(func2)
        def new_func2(*args, **kwargs):
            warnings.simplefilter('always', ExperimentalWarning)
            warnings.warn(
                fmt2.format(name=func2.__name__),
                category=ExperimentalWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', ExperimentalWarning)
            return func2(*args, **kwargs)

        return new_func2

    else:
        raise TypeError(repr(type(reason)))
