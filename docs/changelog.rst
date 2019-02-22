.. include:: .special.rst
Changelog
###############################################

Current Major release
=============================================

`3.0.0`_ (2019-02-21)
---------------------------------------------
* :blue:`rewrite`: Fourth rewrite and redesign (started 2018-09-01)
* :red:`todo`: No workflows done as of yet, planned for 3.1.0
* :red:`todo`: No command line interfaces done as of yet, planned for 3.2.0
* :green:`enhancement`: Support REST and SOAP API types
* :green:`enhancement`: Uses pip for all dependencies, no more bundled libraries
* :green:`enhancement`: Package listed on pypi to allow for pip install
* :green:`enhancement`: Docs now hosted on readthedocs
* :green:`enhancement`: Support for Python v2.7.x and Python v3.7.x
* :green:`enhancement`: Modularity everywhere - no more tightly bundled objects that do everything
* :green:`enhancement`: SSL Certification validation now built-in and required
* :green:`enhancement`: Specialized prompting module for getting user input from console
* :green:`enhancement`: Specialized SSL cert module for getting SSL Certs in PEM format and displaying their contents in a human friendly way (like a browser)

Commit history
---------------------------------------------
.. git_changelog::


Older Major releases
=============================================

`2.0.0`_ (2015-08-07)
---------------------------------------------
* :blue:`rewrite`: Third rewrite and redesign
* Added Tanium Platform v6.2 and v6.5 support
* Automated API workflow capture
* Automated API examples
* Much more

`1.0.0`_ (2014-12-01)
---------------------------------------------
* :blue:`rewrite`: Second rewrite and redesign
* Added more and better workflows
* Re-worked command line interface
* More and better docs

`0.0.5`_ (2014-11-05)
---------------------------------------------
* :blue:`rewrite`: First rewrite and redesign
* Initial testing framework added

.. _Birth:

`0.0.1`_ (2014-10-10)
---------------------------------------------
* :blue:`initial`: Birth of PyTan!
* Only Tanium Platform v6.0 supported

.. _`3.0.0`: https://github.com/tanium/pytan3
.. _`2.0.0`: https://github.com/tanium/pytan/compare/1.0.0...2.0.0
.. _`1.0.0`: https://github.com/tanium/pytan/compare/fde933be0fd00fe7bd6cde1153dc0101e9813bfb...1.0.0
.. _`0.0.5`: https://github.com/tanium/pytan/compare/53a4f87348255ed3be28367d5e323016c53ae4b7...fde933be0fd00fe7bd6cde1153dc0101e9813bfb
.. _`0.0.1`: https://github.com/tanium/pytan/commit/53a4f87348255ed3be28367d5e323016c53ae4b7
