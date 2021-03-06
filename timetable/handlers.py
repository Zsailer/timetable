__doc__ = """
Base module for TimeTable package.
"""
class Handler(object):
    """ Object that manages atttribute data.
    """
    def __init__(self, **attrs):
        self._attrs = {}
        self.addattr(**attrs)

    @property
    def metadata(self):
        """Return attribute metadata (looks the same as self.attrs in this
        parent class)
        """
        return self._attrs

    @property
    def attrs(self):
        return self._attrs

    def addattr(self, **attrs):
        """ Add attribute to Handler
        """
        for key, value in attrs.items():
            self._attrs[key] = value
            setattr(self, key, value)

    def rmattr(self, *attrs):
        """ Remove attribute from Handler.
        """
        for attribute in attrs:
            del self._attrs[attribute]
            delattr(self, attribute)

class ContainerHandler(Handler):
    """ Handler inherited by most objects in this package. Manages
    addition/removal of subobjects.
    """
    def __init__(self, *items, **attrs):
        super(ContainerHandler, self).__init__(**attrs)
        self._contents = {}
        self.add(*items)

    @property
    def metadata(self):
        """Return metadata for this object."""
        metdata = dict(self._attrs)
        for item in self.contents:
            item.attrs

    @property
    def contents(self):
        return self._contents

    @property
    def _type_exception_message(self):
        return """And object already exists in contents with the same ID."""

    @property
    def _prefix(self):
        raise Exception("""Must be implemented in a Subclass.""")

    @property
    def _child_type(self):
        raise Exception("""Must be implemented in a Subclass.""")

    def _check_type(self, item):
        """ Check that the item is an expected object.
        """
        if item.__class__ != self._child_type:
            raise Exception("Argument must be a(n) `" + \
                self._child_type.__name__ + "` object!")

    def _assign_id(self, item):
        """Assigns an `id` to object, with a given prefix.
        """
        # Check that argument is an expected object
        self._check_type(item)
        # If the object doesn't already have an ID, give it one
        if hasattr(item, "id") is False:
            number = 0
            new_id = item._prefix + "%06d" % number   # 9-character ID
            while new_id in self._contents.keys():
                number += 1
                new_id = item._prefix + "%06d" % number
            item.addattr(id=new_id)
        # If ID exists in object, check that it isn't in this object already
        else:
            if item.id in self._contents:
                raise Exception(self._type_exception_message)

    def add(self, *items):
        """Add object to Handler.
        """
        for item in items:
            self._assign_id(item)
            setattr(self, item.id, item)
            self._contents[item.id] = item

    def rm(self, *ids):
        """Remove object with `id` from Handler.
        """
        for id in ids:
            delattr(self, id)
            del self._contents[id]
