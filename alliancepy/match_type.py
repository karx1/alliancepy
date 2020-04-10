import enum


class MatchType(enum.Enum):
    """
    An enum for getting a match from an event. Use like so:\n

    .. code:: py

        from alliancepy import MatchType
        ...

        match = event.match(MatchType.QUALIFICATION, 15) # Gets info on qualifier match 15
    """
    QUALIFICATION = "q"
    ELIMINATION = "e"
