.. include:: .special.rst
Features
########################################

#. Automation

   Create scripts that automate any concept you can think of.

   For example: You can write a script that asks a question, gets the results, and emails it to you. Then you can schedule that script via Task Scheduler/cron/etc to run every night.

#. Integration

   Create seamless integrations with other products.

   For example: You can write an integration with a ticketing system to have it automatically ask a question and include the results in the ticket.

#. Complete API exposure

   Anything that Tanium can do can be done via PyTan.

   It is a complete exposure of the Tanium API, which is what the web browser interface uses to perform all of its functions.

#. Workflow encapsulation

   Workflows remove the need for users of the Tanium API to know how requests must be sent for a given set of operations.

   For instance:

   * Asking a question, waiting for results, and then getting result data can equate to over 100 API calls.
   * Creating a user, assigning it to various RBAC roles, user groups, and so on can take over 30 API calls.

   .. todo::
      No workflows are shipped with PyTan as of yet. It will take time to convert all of the workflows from PyTan 2.x into the new architecture built for PyTan 3.x.

      :green:`Planned for version`: :ref:`3.1.0`

#. Command Line encapsulation around Workflows

   Command Line Interfaces make it so that users of the Tanium API do not even need to know PyTan to utilize the various workflows provided by PyTan.

   There are people in the IT world that prefer to work from a command line. PyTan makes that possible for users of Tanium.

   .. todo::
      No command line interfaces are shipped with PyTan as of yet. The workflows will need to be done first, and then the logic for how to wrap those workflows seamlessly into command line scripts will take some effort.

      :green:`Planned for version`: :ref:`3.2.0`

#. Security

   PyTan version 3 enforces SSL certificate validation for each Tanium server it connects to, and will prompt on the initial connection to a Tanium server for validity by showing information from the certificate and asking the user if it is valid.

   It also provides a secure method for storing credentials to disk at state, making it so that credentials aren't stored in plain text on scripts somewhere on disk.

#. Multiplatform support

   PyTan is written with the goal of working out of the box on all major Operating systems.

#. Python 2 and 3 support

   PyTan version 3 supports both Python 2 and Python 3. Previous versions of PyTan only supported Python 2.

#. Layered concept

   PyTan version 3 has all of its functionality organized into specific :ref:`layers <API Layers>` that build on top of each other.

   This version has 10 layers which make it vastly easier to maintain and extend PyTan, whereas previous versions of PyTan had all of the functionality bundled into one to three layers.

   All layers utilize `Abstract Base Classes <https://docs.python.org/3/library/abc.html>`_ to establish a contract on the implementation of that specific layer.

   This allows each layer to have a well defined interface that enforces each implementation of that layer to work the same. It also makes it easy to support new API types, API commands, API versions, and more.

   For example: Authentication methods, API Clients, API Adapters, API Results, and API objects will each work the same regardless of the underlying implementation.

#. Version checking

   Each layer in PyTan3 that relies on the Tanium API has the ability to specify that the Tanium platform servers version is an exact version, or is at least a minimum version, or is at most a maximum version.

   This allows each object in a layer to specify what version(s) it will work with.

#. Type Checking

   Each layer in PyTan3 that relies on the Tanium API has the ability to specify what type of API it supports.
