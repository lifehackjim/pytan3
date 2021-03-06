# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`pytan3.results`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions
from .. import utils


class ModuleError(exceptions.PyTanError):
    """Parent of all exceptions for :mod:`pytan3.results`.

    Thrown by:
      * :meth:`pytan3.results.RestUrlPath.__init__`
    """

    pass


class ModuleWarning(exceptions.PyTanWarning):
    """Parent of all warnings for :mod:`pytan3.results`.

    Thrown by:
    """

    pass


class ResponseError(ModuleError):
    """Thrown when a response has an general/uncategorized error.

    Thrown by:
      * :meth:`pytan3.results.Result.error_check`
    """

    def __init__(self, result, error):
        """Constructor.

        Args:
            result (:obj:`pytan3.results.Result`):
                Object exception was thrown from.
            error (:obj:`str`):
                Error string.
        """
        self.result = result
        """:obj:`pytan3.results.Result`: Object exception was thrown from."""
        self.error = error
        """:obj:`str`: Error string."""
        self.response_body = utils.tools.trim_txt(
            txt=result.response_body_str.strip(), limit=10000
        )
        """:obj:`str`: Trimmed response body."""
        self.request_object_obj = result.request_object_obj
        """:obj:`object`: Pretty printed objects from request."""

        error = [
            "",
            "-- From: {o}".format(o=result),
            "-- Request objects:\n{o}".format(o=self.request_object_obj),
            "-- Response body: {o}".format(o=self.response_body),
            "-- Error: {o}".format(o=error),
        ]
        self.error = "\n".join(error)
        """:obj:`str`: Error message that was thrown."""
        super(ResponseError, self).__init__(self.error)


class ObjectExistsError(ResponseError):
    """Thrown when a response tells us the object already exists.

    Thrown by:
      * :meth:`pytan3.results.Result.error_check`
    """

    pass


class ObjectNotFoundError(ResponseError):
    """Thrown when a response tells us the object already exists.

    Thrown by:
      * :meth:`pytan3.results.Result.error_check`
    """

    pass


class TextDeserializeError(ModuleError):
    """Thrown when deserializing a string into python object.

    Thrown by:
      * :meth:`pytan3.results.Result.str_to_obj`

    """

    def __init__(self, result, text, src, exc):
        """Constructor.

        Args:
            result (:obj:`pytan3.results.Result`):
                Object exception was thrown from.
            text (:obj:`str`):
                Text that was being deserialized into python object.
            src (:obj:`str`):
                Description of where text came from.
            exc (:obj:`Exception`):
                Exception that occurred during deserialization.
        """
        self.result = result
        """:obj:`pytan3.results.Result`: Object exception was thrown from."""
        self.text = text
        """:obj:`str`: Text that was being deserialized into python object."""
        self.src = src
        """:obj:`str`: Description of where text came from."""
        self.exc = exc
        """:obj:`Exception`: Exception that occurred during deserialization."""

        error = [
            "",
            "-- From: {o}".format(o=result),
            "{src} text:".format(src=src),
            utils.tools.trim_txt(txt=text, limit=10000),
            "-- Unable to deserialize {src} text, error:".format(src=src),
            format(exc),
        ]
        self.error = "\n".join(error)
        """:obj:`str`: Error message that was thrown."""
        super(TextDeserializeError, self).__init__(self.error)


# class ApiDeserializeError(ModuleError):
#     """Thrown when deserializing a python object to a PyTan API object.

#     Thrown by:
#       * :meth:`pytan3.results.Result.obj_to_api`

#     """

#     def __init__(self, result, error):
#         """Constructor.

#         Args:
#             result (:obj:`pytan3.results.Result`):
#                 Object exception was thrown from.
#         """
#         self.result = result
#         """:obj:`pytan3.results.Result`: Object exception was thrown from."""

#         error = [
#             "",
#             "-- From: {o}".format(o=result),
#             "-- Error: {o}".format(o=error),
#         ]
#         self.error = "\n".join(error)
#         """:obj:`str`: Error message that was thrown."""
#         super(ApiDeserializeError, self).__init__(self.error)


class ApiWrongRequestType(ModuleError):
    """Thrown when get result data/object API obj but request is not of that type.

    Thrown by:
      * :meth:`pytan3.results.Result.data_api`
      * :meth:`pytan3.results.Result.object_api`

    """

    def __init__(self, result, error):
        """Constructor.

        Args:
            result (:obj:`pytan3.results.Result`):
                Object exception was thrown from.
        """
        self.result = result
        """:obj:`pytan3.results.Result`: Object exception was thrown from."""

        error = ["", "-- From: {o}".format(o=result), "-- Error: {o}".format(o=error)]
        self.error = "\n".join(error)
        """:obj:`str`: Error message that was thrown."""
        super(ApiWrongRequestType, self).__init__(self.error)


class DictionaryPathError(ModuleError):
    """Thrown when a response has an error when deserializing.

    Thrown by:
      * :meth:`pytan3.results.CommonMixin.get_dict_path`

    """

    def __init__(self, result, obj, path, src, exc):
        """Constructor.

        Args:
            result (:obj:`pytan3.results.Result`):
                Object exception was thrown from.
            obj (:obj:`dict`):
                Dictionary to traverse using path.
            path (:obj:`str`):
                Nested dictionary keys seperated by / to traverse in obj.
            src (:obj:`str`):
                Where obj came from, used in error text.
            exc (:obj:`Exception`):
                Original exception thrown.
        """
        self.result = result
        """:obj:`pytan3.results.Result`: Object exception was thrown from."""
        self.obj = obj
        """:obj:`dict`: Dictionary to traverse using path."""
        self.path = path
        """:obj:`str`: Nested dictionary keys seperated by / to traverse in obj."""
        self.src = src
        """:obj:`str`: Where obj came from."""
        self.exc = exc
        """:obj:`Exception`: Original exception thrown."""

        error = [
            "",
            "Unable to find path '{path}' in {src}:".format(path=path, src=src),
            format(exc),
        ]
        self.error = "\n".join(error)
        """:obj:`str`: Error message that was thrown."""
        super(DictionaryPathError, self).__init__(self.error)
