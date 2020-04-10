.. _match_name:


Match Name Key
--------------

To get details on a match, you will need to specify a match key.

These are in the following form: `letterNUMBER`.


The letter can either be "q" or "e", which stand for either quialification matches or elimination matches, respectively. This is not case sensitive.

The number corresponds to the number of the match, like 024 or 005.

Put together, `q015` means the 15th qualifier match and `e003` means the third elimination match.

This is then used like so:

.. code:: py

	match = event.match("q015")
