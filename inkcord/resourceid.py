import datetime



class ResourceID(int):
    """

    Args:
        integer (int): An integer representing the id of the resource.
    """
    def get_creation_date(self):
        """
        Returns the time since the resource was created from the id, may not be accurate.
        """
        date_ms = self >> 22 + 1420070400000
        date_s = date_ms / 1000
        # this is how the api says to retrieve the date
        return datetime.datetime.fromtimestamp(date_s)
        