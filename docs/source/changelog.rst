Changelog
==========

This is a detailed description of what changed in each version.

.. _vp1p5p2:

v1.5.2
------
- Write cache to file

.. _vp1p5p1:

v1.5.1
------
- Implement cache.
- Bug fixes

.. _vp1p5:

v1.5
-----
- Overhaul Event processor
- Clean up asyncio logic
- Turn properties into coroutines

.. _vp1p4p5:

v1.4.5
------
- Close session before attempting request again

.. _vp1p4p4:

v1.4.4
-------
- Gracefully handle 429 errors
- Use ensure_future rather than manually grabbing event loop

.. _vp1p4p3:

v1.4.3
------
- Set up logging
- Make creating documentation more efficient
- Fix bug where web requests raise a RuntimeError


.. _vp1p4p2:

v1.4.2
------
- Correctly handle matches with six teams (like elimination matches)

.. _vp1p4p1:

v1.4.1
-------
- Diligent bug squashing

.. _vp1p4:

v1.4
-----
- Create :class:`~alliancepy.match.Match` class
- Bug fixes
- Performance improvements

.. _vp1p3p1:

v1.3.1
-------
- Miscellaneous changes
- Minor bug fixes

.. _vp1p3:

v1.3
-----
- Create event class - shows information about a particular FTC event.
- Improve calculation accuracy

.. _vp1p2p1:

v1.2.1
------
- Minor bug fix release

.. _vp1p2:

v1.2
-----
- Create extensions system - this makes it easy to add extensions to the basic usage.
- Create asynchronous extension - see :ref:`aio` for more details.
- Fix bugs and documentation
- Other miscellaneous changes

.. _vp1p1:

v1.1
-----

- Create enum for season-specific calculations to use instead of manually typing the season key
- Rewrite HTTP request method
- Fix season-specific calculations
- Correctly handle exceptions
- Other miscellaneous fixes

.. _vp1p0p1:

v1.0.1
------

- Create WLT calculations for the specified season

.. _vp1p0:

v1.0
-----

- Initial stable release
