from order import place_order
from klines_size import get_last_candles
import time
from config import setup
from klines_size import change_leverage, asset_precision


class Algo:
    def __init__(self, symbol, level, stop_loss, take_profit, risk, side, position_side, interval_str, verbose):
        self.client = setup()
        self.symbol = symbol
        self.level = level
        self.sl = stop_loss
        self.tp = take_profit
        self.risk = risk
        self.side = side
        self.position_side = position_side
        self.interval_str = interval_str
        self.verbose = verbose
        self.precision = asset_precision(self)
        self.leverage = change_leverage(self)


def start_algo(algo):
    if algo.side == "BUY":
        print(f"Starting Algo under_over()...\n")
        under_over(algo)
    elif algo.side == "SELL":
        print(f"Starting Algo over_under()...\n")
        over_under(algo)
    else:
        print("Error in start_algo(), side not recognized")
        return


def under_over(algo):
    if target_limit(algo):
        local_low = float(get_last_candles(algo)[0][3])

        while True:
            wait_for_next_candle(algo)
            candles = get_last_candles(algo)

            if float(candles[1][3]) < local_low:
                local_low = float(candles[1][3])
            elif float(candles[0][1]) < algo.level:
                algo.sl = deviation(algo, local_low)
                place_order(algo, "LIMIT")
                return
    else:
        print("Error in target_limit()")
        return


def over_under(algo):
    if target_limit(algo):
        local_high = float(get_last_candles(algo)[0][2])

        while True:
            wait_for_next_candle(algo)
            candles = get_last_candles(algo)

            if float(candles[1][3]) > local_high:
                local_high = float(candles[1][3])
            elif float(candles[0][1]) > algo.level:
                algo.sl = deviation(algo, local_high)
                place_order(algo, "LIMIT")
                return
    else:
        print("Error in target_limit()")
        return


def target_limit(algo):
    while True:
        try:
            # Fetch latest price data
            candle = get_last_candles(algo)[0]
            close_now = float(candle[4])
            # Compare price to level and execute order if necessary
            if close_now <= algo.level and algo.side == "BUY":
                place_order(algo, "LIMIT")
                return True

            elif close_now >= algo.level and algo.side == "SELL":
                place_order(algo, "LIMIT")
                return True

            elif algo.verbose:
                print(f"Price: {close_now}$ Level: {algo.level}$")

        except Exception as e:
            print(f"Error fetching price data: {e}")
            return False


def wait_for_next_candle(algo):
    now = get_last_candles(algo)[0]
    compare_open = float(now[1])
    # Wait for next candle
    while True:
        try:
            last = get_last_candles(algo)[1]

            if float(last[1]) == compare_open:
                print("\n***Next candle***")
                break
            else:
                time.sleep(1)
        except Exception as e:
            print(f"Error fetching price data: {e}")
            break


def deviation(algo, local_extreme):
    while True:
        open_now = float(get_last_candles(algo)[0][1])
        close = float(get_last_candles(algo)[0][4])

        if algo.side == "BUY":
            if close < local_extreme:
                local_extreme = close
                print(f"New local low: {local_extreme}$")
            elif open_now > algo.level:
                print("buy order placed")
                return local_extreme
            else:
                print(f"Price: {close}$ Open: {open_now}$ Low: {local_extreme}$")
        elif algo.side == "SELL":
            if close > local_extreme:
                local_extreme = close
                print(f"New local high: {local_extreme}$")
            elif open_now < algo.level:
                print("sell order placed")
                return local_extreme
            else:
                print(f"Price: {close}$ Open: {open_now}$ High: {local_extreme}$")
        else:
            print("Error in deviation(), side not recognized")
            return


