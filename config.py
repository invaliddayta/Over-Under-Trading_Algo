import logging
from binance.lib.utils import config_logging
from binance.um_futures import UMFutures


def setup():
    try:
        config_logging(logging, logging.DEBUG)
        key = "GET THIS FROM BINANCE"
        secret = "GET THIS FROM BINANCE"
        sup = UMFutures(key=key, secret=secret)
        return sup

    except Exception as e:
        print(f"Error in setup(): {e}")
        return None
