# -*- coding: utf-8 -*-
"""Workflow encapsulation package for performing actions using the Tanium API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# import datetime

# from ..adapters import results
# from .. import utils


# class Workflow(object):
#     """Pass."""

#     pass


# class CommonMixin(object):
#     """Pass."""

#     def __init__(self, obj, adapter, lvl="info"):
#         """Constructor."""
#         self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
#         self._obj = obj
#         self._adapter = adapter

#     def __str__(self):
#         """Show object info.

#         Returns:
#             (:obj:`str`)

#         """
#         ctmpl = "{c.__module__}.{c.__name__}".format
#         bits = [
#             "obj={}".format(self.obj),
#             "adapter={!r}".format(ctmpl(c=self.adapter.__class__)),
#         ]
#         bits = "(\n  {},\n)".format(",\n  ".join(bits))
#         cls = ctmpl(c=self.__class__)
#         return "{cls}{bits}".format(cls=cls, bits=bits)

#     def __repr__(self):
#         """Show object info.

#         Returns:
#             (:obj:`str`)

#         """
#         return self.__str__()

#     @property
#     def obj(self):
#         """Property for object.

#         Returns:
#             (:obj:`pytan3.api_models.ApiModel`)

#         """
#         return self._obj

#     @property
#     def adapter(self):
#         """Property for Adapter.

#         Returns:
#             (:obj:`pytan3.adapters.Adapter`)

#         """
#         return self._adapter

#     # LATER(!) workthru
#     def _manual_find(self, attr, value, objs, limit=1):
#         matches = [x for x in objs if getattr(x, attr, None) == value]
#         fun = "where {a!r}=={v!r} found in {objs}"
#         fun = fun.format(a=attr, v=value, objs=objs)
#         if not matches:
#             valid = [getattr(x, attr, None) for x in objs]
#             valid = [x for x in valid if x is not None]
#             error = "No matches {fun}, valid: {valid}"
#             error = error.format(fun=fun, valid=valid)
#             raise results.exceptions.ObjectNotFoundError(error)
#         if matches and len(matches) > limit:
#             error = "More than {n} matches found {fun}, found {c}: {found}"
#             error = error.format(n=limit, c=len(matches), fun=fun, found=[])
#             # LATER(!)
#             raise results.exceptions.ObjectNotFoundError(error)
#         return matches[0]


# class User(CommonMixin, Workflow):
#     """Pass."""

#     @classmethod
#     def get_by_id(cls, id, adapter, lvl="info", **kwargs):
#         """Pass."""
#         obj = adapter.objects.User(id=id)
#         result = adapter.api_get(obj=obj, **kwargs)
#         obj = result()
#         cls = cls(obj=obj, adapter=adapter, lvl=lvl)
#         return cls


# """
#     def _dt_from_tanium(self, dtstr):
#         return datetime.datetime.strptime(dtstr, self._objects.dtfmt)

#     def _minutes_ago(self, dtstr):
#         when = self._dt_from_tanium(dtstr)
#         now = datetime.datetime.utcnow()
#         if when > now:
#             ret = 0
#         else:
#             ret = int((now - when).seconds / 60)
#         return ret


# class User(Common, Workflow):
#     @classmethod
#     def get_by_id(cls, adapter, id, opts=None, **kwargs):
#         obj = adapter.objects.User(id=id)
#         result = adapter.get_object(obj=obj, opts=opts)
#         obj = result.get_object()
#         cls = cls(obj=obj, adapter=adapter, **kwargs)
#         return cls

#     @classmethod
#     def get_by_obj(cls, adapter, obj, opts=None, **kwargs):
#         result = adapter.get_object(obj=obj, opts=opts)
#         obj = result.get_object()
#         cls = cls(obj=obj, adapter=adapter, **kwargs)
#         return cls

#     @classmethod
#     def get_by_name(cls, adapter, name, opts=None, **kwargs):
#         objs = cls.get_all(adapter=adapter, opts=opts)
#         obj = cls._manual_find(attr="name", value=name, objs=objs)
#         cls = cls(obj=obj, adapter=adapter, **kwargs)
#         return cls

#     @classmethod
#     def get_all(cls, adapter, opts=None, **kwargs):
#         obj = adapter.objects.UserList()
#         result = adapter.get_object(obj=obj, opts=opts)
#         obj = result.get_object()
#         cls = cls(obj=obj, adapter=adapter, **kwargs)
#         return cls

#     @classmethod
#     def create(cls, adapter, name, display_name=None, opts=None, **kwargs):
#         obj = adapter.objects.User(name=name, display_name=display_name)
#         try:
#             obj = adapter.create_object(obj=obj, opts=opts)
#         except results.exceptions.ObjectAlreadyExistsError:
#             # return pre-existing if already exists
#             # need log entry
#             obj = cls.get_by_name(name=name, opts=opts)

#     @property
#     def display_name(self):
#         return self._obj.display_name

#     @display_name.setter
#     def display_name(self, value):
#         orig = self._obj.display_name
#         if value != orig:
#             self._obj.display_name = value
#             self.save()
#             m = "{obj} Updated display_name from {o!r} to {n!r}"
#             m = m.format(obj=self, o=orig, n=value)
#             self._log.debug(m)

#     # common? abc?
#     def delete(self, opts=None):
#         opts = opts or self._opts
#         self._obj = self.adapter.delete_object(obj=self._obj, opts=opts)
#         return self

#     def refetch(self, opts=None):
#         opts = opts or self._opts
#         self._obj = self.adapter.update_object(obj=self._obj, opts=opts)
#         return self

#     def save(self, opts=None):
#         opts = opts or self._opts
#         self._obj = self.adapter.update_object(obj=self._obj, opts=opts)
#         return self
# """
