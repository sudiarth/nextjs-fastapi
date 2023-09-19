import pandas as pd
from starlette.requests import Request
from starlette.responses import Response
from traceback import print_exception

from . import common

def get_data(pair, param, requests_session):
    try:
        if requests_session is None:
            requests_session = common.Session()
        url = 'https://indodax.com/api/'+pair+'/'+param
        response = requests_session.api_request(url)
        return response
    except Exception:
        return Response("Internal server error", status_code=500)

def getPairs(pair="btc_idr", session=None):
    try:
        response = get_data("", "pairs", requests_session=session)
        for data in response:
            if(data['ticker_id'] == pair):
                return data
    except Exception:
        return Response("Internal server error", status_code=500)

def getSummaries(pair="btc_idr", param="summaries", session=None):
    try:
        get_pairs = getPairs(pair, session=None)
        response = get_data("", param, requests_session=session)
        summaries = {} 
        summaries = response['tickers'][pair]
        summaries["prices_24h"] = response['prices_24h'][get_pairs['id']]
        summaries["prices_7d"] = response['prices_7d'][get_pairs['id']]

        for s in ('high', 'low', 'vol_{}'.format(get_pairs['traded_currency']), 'vol_{}'.format(get_pairs['base_currency']), 'last', 'buy', 'sell', 'prices_24h', 'prices_7d'):
            summaries[s] = float(summaries.get(s))
        for s in ('percent_24h', 'name', 'server_time'):
            summaries[s] = summaries.get(s)

        percent_24h = ((float(summaries['last']) - float(summaries['prices_24h'])) / float(summaries['prices_24h'])) * 100
        summaries['percent_24h'] = round(percent_24h,2)

        return summaries
    except Exception:
        return Response("Internal server error", status_code=500)

def getTicker(pair="btc_idr", session=None):
    try:
        response = get_data(pair, 'ticker', requests_session=session)

        ticker = {}
        for s in ('high', 'low', 'vol_idr', 'last', 'buy', 'sell', 'server_time'):
            ticker[s] = int(response['ticker'].get(s))
        vol_base = "vol_" + pair[:3]
        vol_counter = "vol_" + pair[-3:]
        for s in (vol_base, vol_counter):
            ticker[s] = float(response['ticker'].get(s))

        return ticker
    except Exception:
        return Response("Internal server error", status_code=500)

def getDepth(pair="btc_idr", session=None):
    try:
        depth = get_data(pair, 'depth', requests_session=session)

        asks = pd.DataFrame(depth['sell'])
        asks.rename(columns={0:'price',1:'volume'},inplace=True)
        # asks[['price', 'volume']] = asks[['price', 'volume']].apply(pd.to_numeric)

        bids = pd.DataFrame(depth['buy'])
        bids.rename(columns={0:'price',1:'volume'},inplace=True)
        # bids[['price', 'volume']] = bids[['price', 'volume']].apply(pd.to_numeric)

        return {"Asks": asks, "Bids": bids}
    except Exception:
        return Response("Internal server error", status_code=500)


def getTradeHistory(pair="btc_idr", session=None):
    try:
        history = get_data(pair, 'trades', requests_session=session)

        df = pd.DataFrame(history)
        df.set_index(df.tid.values , drop=False, inplace=True)
        df = df.reindex(columns=['tid', 'date', 'price', 'amount', 'type'])
        # df[['date' , 'price', 'amount', 'tid']] = df[['date' , 'price', 'amount', 'tid']].apply(pd.to_numeric)

        return df
    except Exception:
        return Response("Internal server error", status_code=500)
