Dependencies
###############################################

* :mod:`requests`:

  Used by :ref:`HTTP Client` to send requests.

* :obj:`cert_human.CertStore` and :obj:`cert_human.CertChainStore`:

  Used by :ref:`Certificate verification for HTTP Client` to validate and prompt user for verification of SSL Certificates.

* :mod:`humanfriendly`:

  Used by :ref:`Tools` to show times and file sizes in human readable format.

* `xmltodict <https://github.com/martinblech/xmltodict>`_:

  Used by :ref:`Adapters` and :ref:`Results` to convert XML text into Python dictionaries and back.

* `colorama <https://github.com/tartley/colorama>`_:

  Used by :ref:`Prompting Utilities` to add colors to prompts in order to have them stand out more.

* `privy <https://github.com/ofek/privy>`_:

  Used by :ref:`Crypt Utilities` to provide AES encryption when writing an :ref:`Authentication Store`.

* :mod:`six`:

  Used throughout PyTan to make code work on Python v2 and Python v3.

* `dotenv <https://github.com/theskumar/python-dotenv>`_:

  Used by PyTan to allow use of a ``.env`` file for :ref:`Environment Variables used throughout PyTan`.
