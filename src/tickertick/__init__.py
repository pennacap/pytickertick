import datetime
import typing
import requests
import urllib.parse
from .query import QueryBase


class Story:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.url: str = data["url"]
        self.site: str = data["site"]
        self.time: datetime.datetime = datetime.datetime.fromtimestamp(
            data["time"]/1000.0, tz=datetime.timezone.utc)
        self.favicon_url: typing.Optional[str] = data.get("favicon_url")
        self.tags: list[str] = data["tags"]
        self.similar_stories: list[str] = data.get("similar_stories", [])
        self.title: typing.Optional[str] = data.get("title")
        self.description: typing.Optional[str] = data.get("description")
        self._frozen: bool = True  # Always true
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} "+ (" ".join([i+"="+repr(self.__dict__[i]) for i in self.__dict__ if not i.startswith("_")]))+">"
    def __setattr__(self, __name: str, __value: typing.Any) -> None:
        if hasattr(self, "_frozen"):
            raise AttributeError(
                "Trying to set attribute on a frozen instance")
        return super().__setattr__(__name, __value)


class Ticker:
    def __init__(self, data: dict):
        self.ticker : str = data["ticker"]
        self.company_name : str = data["company_name"]
        self.country : str = data["country"]
        self.chinese_name : typing.Optional[str] = data.get("chinese_name")
        self.cik : typing.Optional[str] = data.get("cik")
        self._frozen: bool = True  # Always true
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} "+ (" ".join([i+"="+repr(self.__dict__[i]) for i in self.__dict__ if not i.startswith("_")]))+">"
    def __setattr__(self, __name: str, __value: typing.Any) -> None:
        if hasattr(self, "_frozen"):
            raise AttributeError(
                "Trying to set attribute on a frozen instance")
        return super().__setattr__(__name, __value)
    
def get_tickers(query: typing.Optional[str] = None, no: typing.Optional[int] = None) -> list[Ticker]:
    query_dict = {}
    if query:
        query_dict['p'] = query
    if no:
        query_dict['n'] = no
    req = requests.get("https://api.tickertick.com/tickers?" +
                       urllib.parse.urlencode(query_dict))
    if not req.ok:
        raise Exception({
            400: req.text,
            429: "You are being rate limited"
        }[req.status_code])
    return [Ticker(i) for i in req.json()["tickers"]]


def get_feed(query: typing.Optional[typing.Union[str, QueryBase]] = None, no : typing.Optional[int] = None, last_story : typing.Optional[str] = None, hours_ago : int = None, do_multiple : bool = True) -> list[Story]:
    """Fetch the feed from TickerTick

    Args:
        query (str | QueryBase, optional): The query string to fetch (https://github.com/hczhu/TickerTick-API#the-query-language). Defaults to None.
        no (int, optional): The number of stories to fetch. Defaults to None.
        last_story (str, optional): Fetch stories older than the story with this ID. Defaults to None.
        hours_ago (int, optional): Fetch stories older than this. Defaults to None.
        do_multiple (bool, optional): Whether multiple requests should be made to the API to reach the number. Defaults to True.

    Returns:
        list[Story]: The list of stories
    """
    query_dict = {}
    if query:
        query_dict['q'] = str(query)
    no = no or 42
    query_dict['n'] = no
    if last_story:
        query_dict['last'] = last_story
    if hours_ago:
        query_dict['hours_ago'] = hours_ago

    stories = []
    while len(stories) < no:
        query_dict['n'] = no - len(stories)
        req = requests.get("https://api.tickertick.com/feed?" +
                       urllib.parse.urlencode(query_dict))
        if not req.ok:
            raise Exception({
                400: req.text,
                429: "You are being rate limited"
            }[req.status_code])
            
        stories += [Story(i) for i in req.json()["stories"]]
        try:
            query_dict['last'] = stories[-1].id
        except:
            pass
        if not do_multiple:
            break
    return stories
