.. include:: .special.rst
API Layers
##############################

#. :ref:`HTTP Client`

   The lowest layer and the core foundation of PyTan that handles sending and receiving requests using the `requests <http://docs.python-requests.org/en/master/>`_ package. It provides SSL certificate validation and user verification similar to a web browser, recording of requests and responses to files, and more.

#. :ref:`Authentication methods`

   Authentication methods use an **HTTP Client** to authenticate against a Tanium platform server and receive a session token. They provide functionalities such as login, logout, logout all, and validate token.

#. :ref:`Authentication Store`

   The Authentication Store provides a secure way to store an **Authentication method**.

#. :ref:`API clients`

   API clients use an **HTTP Client** and an **Authentication Method** to communicate with a specific type of API.

   API Clients know how to communicate with a specific API path, but do not have any native ability to construct the request bodies or parse the response bodies.

#. :ref:`API Object Modules`

   API Object Modules contain the object definitions used by the Tanium API as native Python objects.

   They are automatically generated using the WSDL for a given Tanium Platform version, and can be modified to work with a specific platform version and API type.

#. :ref:`Models for API Object Modules`

   API Models provide the base classes that make API Objects work like Python objects. They contain the functionality for list objects from the Tanium API to work like Python lists, and for item objects from the Tanium API to work like Python objects with each of the defined attributes from the API exposed as attributes on the object.

#. :ref:`Adapters`

   Adapters use an **API client** combined with an **API object module** to create and send requests. Adapters are responsible for:

   * Exposing API commands like get, add, delete, modify, and more.
   * Converting (serializing) a Python object from an **API object module** into a text string.
   * Creating a request body that contains the converted python object in a format that a given type of API understands.
   * Sending the request body using an **API client** and returning the response in a **Result**.

#. :ref:`Results`

   Results are heavily tethered to an **Adapter**, and are responsible for:

   * Checking for errors in the response and throwing the appropriate exception when an object already exists, an object is not found, a request was not properly formed, or a response returned an error.
   * Parsing the response from a request sent by an **Adapter** into a Python dictionary object.
   * Converting (deserializing) the objects or data set in the response into a Python object from an **API object module**.

#. :ref:`Workflows`

   Workflows rely on an **Adapter** and encapsulate all of the steps needed to perform complex operations into one function. A number of workflows are planned:

   * Adding, updating, deleting users, groups, RBAC, dashboards, and more...
   * Asking saved questions and getitng the answers back in various output forms
   * Asking parsed questions and getitng the answers back in various output forms
   * Asking manually crafted questions and getitng the answers back in various output forms
   * And more...

   .. todo::
      No workflows are shipped with PyTan as of yet. It will take time to convert all of the workflows from PyTan 2.x into the new architecture built for PyTan 3.x.

      :green:`Planned for version`: :ref:`3.1.0`

#. :ref:`Command Line Interfaces`

   The highest layer that provides Python scripts that expose **Workflows** to command line users and removes the need for a user to know how to program in Python in order to utilize PyTan.

   .. todo::
      No command line interfaces are shipped with PyTan as of yet. The workflows will need to be done first, and then the logic for how to wrap those workflows seamlessly into command line scripts will take some effort.

      :green:`Planned for version`: :ref:`3.2.0`
