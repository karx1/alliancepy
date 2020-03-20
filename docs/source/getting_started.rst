Getting started with alliancepy
===============================

The first thing you need to do is get an API key. To do this, go to `The Orange Alliance website <https://theorangealliance.org/home>`__ and register an account. Then, go to your account page and click "get an API Key." It should give you an API key, which you can then use to create your client object.

Now, we need to install the library:

.. code:: bash

	pip install alliancepy

Then, create a new file and create a client object:

.. code:: py

	import alliancepy

	client = alliancepy.Client(api_key="Your API key goes here", application_name="Name of the application/script")

Now, you can create a team object.

.. code:: py

	team = client.team(16405)

This team object has a variety of attributes that you can learn more about in the other pages of this documentation.
Enjoy!