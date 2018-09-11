import requests
from nexus_stats.profile import Profile
from nexus_stats.exceptions import *

class Requester():
    """Represents a connection to the API.
        This class is used to get data from the API and return useful information.
        A few options can be passed to :class:`Requester` to make it easier to use the functions.
        Parameters
        ----------
        user_name : Optional[str]
            The default username used for any request username related.
            If not given, it will be needed when a username related function is called.
        Attributes
        -----------
        url : [str]
            The base url used for the API.

        user_name : Optional[str]
            The username given when the instance is created.
            If none is given, defaults to None.
        """
    def __init__(self, **options):
        self.url = "https://api.nexus-stats.com"
        self.user_name = options.get("user_name", None)

    def get_user_profile(self, userName = None):
        if not userName and not self.user_name:
            raise MissingInput("get_user_profile", "userName")

        if not userName:
            userName = self.user_name

        response = Profile(self.url, userName)
        return response
