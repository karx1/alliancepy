Setting Up Logging
==================

`alliancepy` logs errors and warnings through the `logging <https://docs.python.org/3/library/logging.html#module-logging>`_ python module. It is strongly recommended that the logging module is configured, as it allows you to see various debug messages and errors and warnings. Configuration of the logging module can be as simple as:

.. code:: py

	import logging

	logging.basicConfig(level=logging.INFO)

Placed at the start of the application. This will output the logs from alliancepy as well as other libraries that use the ``logging`` module directly to the console.


The optional ``level`` argument specifies what level of events to log out and can any of ``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO``, and ``DEBUG`` and if not specified defaults to ``WARNING``.


More advanced stups can be used with the `logging <https://docs.python.org/3/library/logging.html#module-logging>`_ module. For example, to output the logs to a file called ``alliancepy.log`` instead of outputting them to the console, the following snipper can be used:

.. code:: py

	import alliancepy
	import logging

	logger = logging.getLogger("alliancepy")
	logger.setLevel(logging.DEBUG
	handler = logging.FileHandler(filename="alliancepy.log", encoding="utf-8", mode="w")
	handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
	logger.addHandler(handler)

This is recommended, especially at verbose levels such as ``INFO``, and ``DEBUG`` as there are a lot of events logged and it would clog the stdout of your program.


For more information, check out the documentation of the `logging <https://docs.python.org/3/library/logging.html#module-logging>`_ module.