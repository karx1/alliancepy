alliancepy
==========


A library to access The Orange Alliance API.
This module makes it easy to access the official First Tech Challenge database and use it in your Python projects for things like data science and more.

Install with:

.. code:: bash
  
  pip install alliancepy
 
Here's a simple example:

.. code:: py
  
  import alliancepy
  
  client = alliancepy.Client(api_key="api_key_goes_here", application_name="application_name_goes_here")
  team = client.team(7172)
  print(team.opr(1920))

Supports
--------
Supports Python 3.6 and up.
