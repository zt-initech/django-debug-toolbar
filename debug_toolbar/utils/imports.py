from __future__ import absolute_import, unicode_literals


def _dot_lookup(thing, comp, import_path):
    try:
        return getattr(thing, comp)
    except AttributeError:
        __import__(import_path)
        return getattr(thing, comp)


def import_string(target):
    components = target.split('.')
    import_path = components.pop(0)
    thing = __import__(import_path)

    for comp in components:
        import_path += ".%s" % comp
        thing = _dot_lookup(thing, comp, import_path)
    return thing


def get_name_from_obj(obj):
    if hasattr(obj, '__name__'):
        name = obj.__name__
    elif hasattr(obj, '__class__') and hasattr(obj.__class__, '__name__'):
        name = obj.__class__.__name__
    else:
        name = '<unknown>'

    if hasattr(obj, '__module__'):
        module = obj.__module__
        name = '%s.%s' % (module, name)

    return name
