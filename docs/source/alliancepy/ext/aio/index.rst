.. _aio:

alliancepy "aio" extension
==========================

This extension provides and Asynchronous version of the normal alliancepy classes. This is so you can use it in things like web servers and more.

To install alliancepy with the asynchronous capabilities, use:

.. code:: bash

	pip install alliancepy[async]

This will install aiohttp with speedups, and nest_asyncio. See :ref:`install` for more information.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   async_client
   async_team
   async_event
   async_match