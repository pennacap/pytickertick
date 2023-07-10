import enum

class StoryTypes(enum.Enum):
    CURATED = "curated"
    EARNING = "earning"
    MARKET = "market"
    SEC = "sec"
    SEC_FIN = "sec_fin"
    TRADE = "trade"
    UGC = "ugc"
    ANALYSIS = "analysis"
    INDUSTRY = "industry"

class QueryBase:
    pass

class AndOrBase(QueryBase):
    operator : str
    def __init__(self, *args):
        self._args = args
        if len(args) == 0:
            raise ValueError("must have atleast 1 argument")
    @property
    def args(self):
        return map(str, self._args)
    @args.setter
    def args_setter(self, value):
        if len(value) == 0:
            raise ValueError("must have atleast 1 argument")
        self._args = value
        
    def __str__(self) -> str:
        return f'({self.operator} ' + (' '.join(self.args))+')'


class Or(AndOrBase):
    operator : str = "or"

class And(AndOrBase):
    operator : str = "and"

class Diff(QueryBase):
    def __init__(self, query1, query2):
        self.query1 = query1
        self.query2 = query2
    def __str__(self) -> str:
        return f'(diff {repr(self.query1)[1:-1]} {repr(self.query2)[1:-1]})'
    
class Ticker(QueryBase):
    def __init__(self, ticker : str):
        self.ticker = ticker
    def __str__(self) -> str:
        return f'z:{repr(self.ticker)[1:-1]}'

class BroadTicker(QueryBase):
    def __init__(self, ticker : str):
        self.ticker = ticker
    def __str__(self) -> str:
        return f'tt:{repr(self.ticker)[1:-1]}'


class Site(QueryBase):
    def __init__(self, site : str):
        self.site = site
    def __str__(self) -> str:
        return f's:{repr(self.site)[1:-1]}'

class Entity(QueryBase):
    def __init__(self, entity : str):
        self.entity = entity
    def __str__(self) -> str:
        return f'e:{repr(self.entity.replace(" ", "_").lower())[1:-1]}'

class StoryType(QueryBase):
    def __init__(self, story_type : StoryTypes) -> None:
        self.story_type = story_type
    def __str__(self) -> str:
        return f'T:{self.story_type.value}'

