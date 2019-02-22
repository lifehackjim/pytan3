Release Strategy
##################################################

All releases will have tags and branches named after their version number, and will also be published on the `releases page <https://github.com/tanium/pytan3/releases>`_.

Major releases
==================================================
A major release will include breaking changes. If the previous release was v2.0.0 the next version will be v3.0.0.

Breaking changes are changes that break backwards compatibility with prior versions. If an API command was removed or the interface for a layer is completely different, that would only happen in a Major release.

Major releases may also include miscellaneous bug fixes. The core developers of PyTan are committed to providing a good user experience. This means we’re also committed to preserving backwards compatibility as much as possible. Major releases will be infrequent and will need strong justifications before they are considered.

With that in mind, PyTan `version 3 <https://github.com/tanium/pytan3>`_ is a major release and as such has a vastly different architecture than `version 2 <https://github.com/tanium/pytan>`_.

Any scripts that were written to use version 2 will not work with version 3.

Minor releases
==================================================
A minor release will not include breaking changes but may include miscellaneous bug fixes. If the previous version of PyTan released was v3.1.0 a minor release would be versioned as v3.2.0.

Minor releases will be backwards compatible with releases that have the same major version number. In other words, all versions that would start with v3. should be compatible with each other.

Micro releases
==================================================
A micro release will only include bug fixes that were missed when the previous version was released. If the previous version of PyTan released v3.1.0 the hotfix release would be versioned as v3.1.1.


