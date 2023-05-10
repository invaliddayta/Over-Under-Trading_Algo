import logging
from binance.error import ClientError
from datetime import datetime, timedelta
import time


def get_last_candles(algo):
    try:
        interval = algo.interval_str.split('m')[0]
        # Initialize UMFuturesClient
        time.sleep(0.1)
        # Calculate the start and end times for the candle
        now = datetime.now()
        end_time = now - timedelta(minutes=now.minute % int(interval), seconds=now.second, microseconds=now.microsecond)
        start_time = end_time - timedelta(minutes=int(interval))

        # Convert datetime objects to timestamp in milliseconds
        start_timestamp = int(start_time.timestamp() * 1000)
        end_timestamp = int(end_time.timestamp() * 1000)

        # Get kline/candlestick data for the given symbol and time range
        candles = algo.client.klines(symbol=algo.symbol, interval=algo.interval_str, start_time=start_timestamp,
                                     end_time=end_timestamp, limit=2)

        if candles:
            now_candle = candles[-1]
            prev_candle = candles[-2]
            return now_candle, prev_candle

        else:
            raise ValueError(f"No candles found for symbol {algo.symbol} in the last {algo.interval_str}.")
    except ClientError as e:
        # Handle any API errors
        print(f"Error occurred while getting last {algo.interval_str} candle: {e}")


def change_leverage(algo):
    print(f"Changing leverage to Max Leverage...")
    try:
        leverage = get_max_leverage(algo)
        response = algo.client.change_leverage(leverage=leverage, symbol=algo.symbol)
        logging.info(response)
        print(f"Leverage changed to {leverage}x")
        return leverage

    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def get_max_leverage(algo):
    try:
        response = algo.client.leverage_brackets(symbol=algo.symbol)
        max_leverage = (response[0]['brackets'][0]['initialLeverage'])
        return max_leverage

    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def asset_precision(algo):
    print(f"Getting asset precision for {algo.symbol}")
    asset_info = algo.client.exchange_info()
    for asset in asset_info['symbols']:
        if asset['symbol'] == algo.symbol:
            print(f"Asset precision: {asset['quantityPrecision']}")
            return asset['quantityPrecision']


def calculate_size(algo):
    if algo.side == "BUY":
        size = algo.risk / (algo.level - algo.sl)
        return size

    elif algo.side == "SELL":
        size = algo.risk / (algo.sl - algo.level)
        return size
    else:
        print("Error in calculate_size(), side not recognized")
        return 0
