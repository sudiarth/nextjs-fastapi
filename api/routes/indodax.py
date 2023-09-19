from fastapi import APIRouter
from decouple import config

import api.indodax as indodax

akun = indodax.TradeAPI(config("INDODAX_API_KEY"),
                        config("INDODAX_SECRET_KEY"))

router = APIRouter(
    prefix="/indodax",
    tags=["indodax"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get-pairs")
def get_pairs(pair='btc_idr'):
    return indodax.getPairs(pair)

@router.get("/get-summaries")
def get_summaries(pair='bnb_idr'):
    return indodax.getSummaries(pair)

@router.get("/get-ticker/{pair}")
def get_ticker(pair):
    return indodax.getTicker(pair)

@router.get("/get-depth")
def get_depth(pair='bnb_idr'):
    return indodax.getDepth(pair)

@router.get("/get-trade-history")
def get_trade_history(pair='bnb_idr'):
    return indodax.getTradeHistory(pair)

@router.get("/get-info")
def get_info():
    return akun.getInfo()


@router.get("/trade-history")
def trade_history(pair='bnb_idr'):
    return akun.tradeHistory(pair)


@router.get("/order-history/{pair}")
def order_history(pair='bnb_idr'):
    return akun.orderHistory(pair)