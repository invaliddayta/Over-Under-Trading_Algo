import logging
from binance.error import ClientError
from klines_size import calculate_size


def place_order(algo, order_type):
    quantity = round(calculate_size(algo), algo.precision)
    send_order(algo, order_type, quantity)
    asset = algo.symbol.replace("USDT", "")
    print("*" * 50)
    print(
        f"{order_type} {algo.side} {algo.position_side} Order placed at:{algo.level}, amount:{quantity}{asset}, notional:{algo.level * quantity}$")
    print(f"SL:{algo.sl}$, TP:{algo.tp}$")
    print("*" * 50)


def send_order(algo, order_type, quantity):
    if algo.position_side == "SHORT":
        tp_side = "BUY"
        tp_direction = "LONG"
    elif algo.position_side == "LONG":
        tp_side = "SELL"
        tp_direction = "SHORT"
    else:
        print("Error in send_order(), position_side not recognized")
        return

    try:
        order = {
            "symbol": algo.symbol,
            "side": algo.side,
            "positionSide": algo.position_side,
            "type": order_type,
            "quantity": quantity,
            "timeInForce": "GTC",
            "price": algo.level,
        }

        stop_order = {
            'symbol': algo.symbol,
            'side': tp_side,
            'type': 'STOP_MARKET',
            "positionSide": tp_direction,
            'quantity': quantity,
            'stopPrice': algo.sl,
        }

        take_profit_order = {
            "symbol": algo.symbol,
            "side": tp_side,
            "positionSide": tp_direction,
            "type": 'TAKE_PROFIT_MARKET',
            "quantity": quantity,
            "timeInForce": "GTC",
            "stopPrice": algo.tp,
        }

        response = algo.client.new_order(**order)
        response_s = algo.client.new_order(**stop_order)
        response_t = algo.client.new_order(**take_profit_order)

        logging.info('Response: %s, Response_t: %s, Response_s: %s', response, response_t, response_s)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )






