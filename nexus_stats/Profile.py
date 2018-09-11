import requests
from nexus_stats.exceptions import *

class Accolades():
    """The class used to represent a user's markings.
            Attributes
            -----------
            founder : [str]
                If the user has a founder badge, and if they do, what tier. Is `False` if the user has no founder badge.
                Can be any of the following: `Disciple`, `Hunter`, `Master`, `Grand Master`, `False`.

            guide : [bool]
                If the user has a guide badge. Is `False` if the user has no guide badge.
                Can be `Senior Guide of the Lotus` or `Junior Guide of the Lotus`.

            moderator : [bool]
                If the user has been marked for death by zanuka.

            partner : [bool]
                If the user has the partner badge.

            staff : [bool]
                If the user has the staff badge."""
    def __init__(self, data):
        self.founder = data["founder"]
        self.guide = data["guide"]
        self.moderator = data["moderator"]
        self.partner = data["partner"]
        self.staff = data["staff"]

class Rank():
    """The class used to represent a user's rank.
            Attributes
            -----------
            name : [str]
                The rank's name. Not to be confused with :class:`Profile.name`.

            number : [int]
                The mastery rank number.

            next : [bool]
                If the user has been marked for death by zanuka."""
    def __init__(self, data):
        self.name = data["name"]
        self.number = data["number"]
        self.next = data["next"]

class Mastery():
    """The class used to represent a user's mastery.
            Attributes
            -----------
            rank : [:class:`Rank`]
                The user's rank as a :class:`Rank`.

            xp : [int]
                Amount of total mastery earned.

            xpRemaining : [int]
                Amount of mastery remaining."""
    def __init__(self, data):
        self.rank = Rank(data=data["rank"])
        self.xp = data["xp"]
        self.xpRemaining = data["xpUntilNextRank"]

class Clan():
    """The class used to represent a user's clan.
            Attributes
            -----------
            name : [str]
                The clan's name. Not to be confused with :class:`Profile.name`

            rank : [int]
                The clan's rank.

            type : [str]
                The size of clan."""
    def __init__(self, data):
        self.name = data["name"]
        self.rank = data["rank"]
        self.type = data["type"]

class Marked():
    """The class used to represent a user's markings.
        Attributes
        -----------
        stalker : [bool]
            If the user has been marked for death by the stalker.

        g3 : [bool]
            If the user has been marked for death by the g3.

        zanuka : [bool]
            If the user has been marked for death by zanuka."""
    def __init__(self, data):
        self.stalker = data["stalker"]
        self.g3 = data["g3"]
        self.zanuka = data["zanuka"]

class Profile():
    """The main class used to represent a user's profile.
        Parameters
        ----------
        url : [str]
            The base URL for the API. This is already given in :class:`Requester`.
        Attributes
        -----------
        url : [str]
            The base url used for the API.

        ext : [str]
            The endpoint used. This is made using the `userName` given in :class:`Requester`.

        dataURL : [str]
            The full URL used to get `data`.

        name : [str]
            The username of the user's data being used.

        accolades : [:class:`Accolades`]
            The :class:`accolades` class with all data on the user's accolades.

        mastery : [:class:`Mastery`]
            The :class:`Mastery` class with all data on the user's mastery.

        clan : [:class:`Clan`]
            The :class:`Clan` class with all data on the user's clan.

        marked : [:class:`Marked`]
            The :class:`Marked` class with all data on the user's marks.

        createdAt : [str]
            The time of when the data was created.

        updatedAt : [str]
            The last time the user's data was updated."""
    def __init__(self, url, userName):
        self.url = url
        self.ext = "/warframe/v1/players/{}/profile".format(userName)
        self.dataURL = self.url + self.ext

        try:
            response = requests.get(self.dataURL)
            data = response.json()

        except requests.exceptions.MissingSchema:
            raise ServerException("Link not found.")


        try:
            r = data["reason"]
            self.data = None
            if r == "Could not find user in-game.":
                raise UserNotFound()

        except KeyError:
            self.data = data

            if "E: Not Detected" in data:
                # TODO Find field
                pass

            self.name = data["name"]
            self.accolades = Accolades(data=data["accolades"])
            self.mastery = Mastery(data=data["mastery"])
            self.clan = Clan(data=data["clan"])
            self.marked = Marked(data=data["marked"])
            self.createdAt = data["createdAt"]
            self.updatedAt = data["updatedAt"]
