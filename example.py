import threading
import random
import time

class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type  
        self.ticker = ticker
        self.quantity = quantity
        self.price = price

class StockOrderBook:
    def __init__(self):
        self.orders = []  
        self.lock = threading.Lock()

    def addOrder(self, order_type, ticker, quantity, price):
        order = Order(order_type, ticker, quantity, price)
        with self.lock:
            self.orders.append(order)
        print(f"Order Added: {order_type} {ticker} {quantity} @ {price}")
        self.matchOrder()

    def matchOrder(self):
        with self.lock:
            buys = [o for o in self.orders if o.order_type == "Buy"]
            sells = [o for o in self.orders if o.order_type == "Sell"]
            buys.sort(key=lambda x: -x.price)
            sells.sort(key=lambda x: x.price)
            i, j = 0, 0
            while i < len(buys) and j < len(sells):
                if buys[i].ticker == sells[j].ticker and buys[i].price >= sells[j].price:
                    matched_quantity = min(buys[i].quantity, sells[j].quantity)
                    print(f"Matched: {matched_quantity} shares of {buys[i].ticker} at {sells[j].price}")
                    buys[i].quantity -= matched_quantity
                    sells[j].quantity -= matched_quantity
                    if buys[i].quantity == 0:
                        i += 1
                    if sells[j].quantity == 0:
                        j += 1
                else:
                    break
            self.orders = [o for o in self.orders if o.quantity > 0]

def random_order_generator(order_book):
    tickers = [f"STOCK{i}" for i in range(1, 1025)]
    while True:
        order_type = random.choice(["Buy", "Sell"])
        ticker = random.choice(tickers)
        quantity = random.randint(1, 100)
        price = round(random.uniform(10, 500), 2)
        order_book.addOrder(order_type, ticker, quantity, price)
        time.sleep(random.uniform(0.1, 0.5)) 

if __name__ == "__main__":
    order_book = StockOrderBook()
    for _ in range(5):
        threading.Thread(target=random_order_generator, args=(order_book,), daemon=True).start()
    time.sleep(10)
