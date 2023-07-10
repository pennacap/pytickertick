# PyTickerTick : An API wrapper for the [TickerTick API](https://github.com/hczhu/TickerTick-API) in Python
## Installation
```sh
pip install pytickertick
```

## Usage
```py
import tickertick as tt
import tickertick.query as query
ticker1 = tt.get_tickers(
    query = 'Ama',
    no = 5
) # Search for any tickers matching 'Ama'

ticker2 = tt.get_tickers(
    query = 'aa',
    no = 2
) # Search for any tickers matching 'aa'

feed1 = tt.get_feed(
    query = query.And(
        query.BroadTicker('aapl'),
        query.StoryType(query.StoryTypes.SEC)
    )
) # SEC filings from Apple Inc.

feed2 = tt.get_feed(
    query = query.Or(
        query.BroadTicker('meta'),
        query.BroadTicker('aapl'),
        query.BroadTicker('amzn'),
        query.BroadTicker('nflx'),
        query.BroadTicker('goog')
    )
) # News stories about FAANG stocks	

feed3 = tt.get_feed(
    query = query.And(
        query.Or(
            query.BroadTicker('meta'),
            query.BroadTicker('goog'),
        ),
        query.Site('reddit')
    )
) # News stories about Meta (meta) and Google (goog) from reddit.com	

feed4 = tt.get_feed(
    query = query.Diff(
        query.Or(
            query.BroadTicker('meta'),
            query.BroadTicker('goog'),
        ),
        query.Site('reddit')
    )
) # News stories about Meta (meta) and Google (goog) not from reddit.com	

feed5 = tt.get_feed(
    query = query.Diff(
        query.Entity('Elon Musk')
        query.Site('nytimes')
    )
) # Stories with Elon Musk in titles not from NY Times	
```

