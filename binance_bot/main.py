from config import API_KEY, API_SECRET
from logger import setup_logger
from bot import BasicBot

def get_user_input():
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter side (BUY/SELL): ").upper()
    order_type = input("Enter order type (MARKET/LIMIT): ").upper()
    quantity = float(input("Enter quantity: "))
    price = None
    if order_type == 'LIMIT':
        price = input("Enter limit price: ")

    return symbol, side, order_type, quantity, price

if __name__ == "__main__":
    logger = setup_logger()
    bot = BasicBot(API_KEY, API_SECRET)

    symbol, side, order_type, quantity, price = get_user_input()
    order = bot.place_order(symbol, side, order_type, quantity, price)
    if order:
        print("Order successfully placed:")
        print(order)
    else:
        print("Order placement failed.")