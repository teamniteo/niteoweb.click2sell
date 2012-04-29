Changelog
=========

0.4.2 (2012-04-29)
------------------

- Made ``click2sell key`` non-required so we can modify the product_id to
  group_name mapping without always supplying the ``click2sell key``.
  [zupo]

- Even more work on groups edge-cases.
  [zupo]


0.4.1 (2012-04-22)
------------------

- More tests for groups edge-cases.
  [zupo]

- Updating package with latest best practices.
  [zupo]


0.4 (2012-04-21)
----------------

- Site admins can now map C2S ``product_id`` to groups. This causes new members
  to be added to the group their ``product_id`` maps to.
  [zupo]

- Store configuration in `plone.app.registry` rather than in a local utility.
  [zupo]


0.3 (2012-01-28)
----------------

- Updated the package with latest best practices, added support for
  `plone.app.testing`, moved to GitHub.
  [zupo]


0.2.2 (2011-08-16)
------------------

- Support for Plone 4.1.
  [zupo]


0.2.1 (2010-10-06)
------------------

- Fixed updating an already existing member.
  [zupo]

- Added Uninstall profile.
  [zupo]


0.2 (2010-10-06)
----------------

- Polishing, adding tests.
  [zupo]


0.1 (2010-09-30)
----------------

- Initial release.
  [zupo]

