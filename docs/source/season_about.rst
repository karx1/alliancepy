.. _season_about:

Season-specific calculations
============================

Some calculations require you to input a Season. This can be done with the Season enum.
For example,

.. code:: py

	import alliancepy
	from alliancepy import Season

	client = alliancepy.Client(...)
	team = client.team(...)

	print(team.season_wins(Season.SKYSTONE))

This makes it easier to access season-specific calculations without having to figure out the season key.