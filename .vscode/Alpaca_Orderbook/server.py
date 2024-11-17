# pip3 install asyncio websockets certifi typing
import asyncio
import websockets
import ssl
import json
from dotenv import load_dotenv
import os
import certifi
import time
from collections import defaultdict
import os
from typing import Union

# load alpaca api key/secret key from .env file
load_dotenv('creds.env')

class BTCOrderBookDisplay:
    def __init__(self):
        self.uri = "wss://stream.data.alpaca.markets/v1beta3/crypto/us"
        self.api_key = os.getenv('ALPACA_API_KEY')
        self.api_secret = os.getenv('ALPACA_API_SECRET')
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        # order book states
        self.bids = defaultdict(float)
        self.asks = defaultdict(float)
        self.last_update = None
        
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def format_price(self, price):
        return f"${price:,.2f}"
    
    def format_quantity(self, qty):
        return f"{qty:.4f}"
    
    def display_orderbook(self):
        self.clear_terminal()
        
        # terminal visual header
        print("\n" + "="*80)
        print(f"BITCOIN/USD ORDER BOOK - Last Update: {self.last_update}")
        print("="*80)
        
        # sorted bids and asks by price
        sorted_bids = sorted(self.bids.items(), reverse=True)
        sorted_asks = sorted(self.asks.items())
        
        # top 15 levels from buy/sell side to rperesent l2 orderbook
        bids_display = sorted_bids[:15]
        asks_display = sorted_asks[:15]
        
        # calculate max length
        max_price_len = max(
            len(self.format_price(max([p for p, _ in bids_display + asks_display], default=0))),
            len("PRICE")
        )
        max_qty_len = max(
            len(self.format_quantity(max([q for _, q in bids_display + asks_display], default=0))),
            len("QUANTITY")
        )
        
        # the terminal visual headers for bid prices and quanitity
        print("\nBIDS" + " "*(max_price_len + max_qty_len - 4))
        print(f"{'PRICE':<{max_price_len}} {'QUANTITY':<{max_qty_len}}")
        print("-" * (max_price_len + max_qty_len + 2))
        
        # print out the terminal visuals for the bids
        for price, quantity in bids_display:
            print(f"\033[32m{self.format_price(price):<{max_price_len}} {self.format_quantity(quantity):<{max_qty_len}}\033[0m")
            
        print("\nASKS" + " "*(max_price_len + max_qty_len - 4))
        print(f"{'PRICE':<{max_price_len}} {'QUANTITY':<{max_qty_len}}")
        print("-" * (max_price_len + max_qty_len + 2))
        
        # print out the terminal visuals for the asks
        for price, quantity in asks_display:
            print(f"\033[31m{self.format_price(price):<{max_price_len}} {self.format_quantity(quantity):<{max_qty_len}}\033[0m")
            
    async def connect(self):
        async with websockets.connect(
            self.uri,
            ssl=self.ssl_context,
            ping_interval=None
        ) as websocket:
            # auth message following current alpaca crypto market data stream docs
            auth_message = {
                "action": "auth",
                "key": self.api_key,
                "secret": self.api_secret
            }
            
            await websocket.send(json.dumps(auth_message))
            print("Connecting to Alpaca Crypto WebSocket...")
            
            # new subscription format from alpaca docs
            subscribe_message = {
                "action": "subscribe",
                "trades": ["BTC/USD"],
                "quotes": ["BTC/USD"],
                "orderbooks": ["BTC/USD"]
            }
            
            await websocket.send(json.dumps(subscribe_message))
            print("Subscribed to BTC/USD orderbook")
            
            try:
                while True:
                    message = await websocket.recv()
                    await self.handle_message(message)
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed")
                
    async def handle_message(self, message: str) -> None:
        try:
            msg = json.loads(message)
            print(f"Debug - Received message: {msg}")  # checking for client recieviing the msg
            
            # incase there is an array of messages
            if isinstance(msg, list):
                for m in msg:
                    await self.process_single_message(m)
            else:
                await self.process_single_message(msg)
                    
        except Exception as e:
            print(f"Error processing message: {e}")
            print(f"Message was: {message}")
            
    async def process_single_message(self, msg: Union[dict, list]) -> None:
        if isinstance(msg, dict):
            # auth response handling
            if msg.get('msg') == 'authenticated':
                print("Successfully authenticated")
                return
            
            # error handling for response
            if msg.get('T') == 'error':
                error_code = msg.get('code')
                error_msg = msg.get('msg')
                print(f"Error {error_code}: {error_msg}")
                if error_code == 401:
                    print("Please authenticate before subscribing.")
                elif error_code == 402:
                    print("Authentication failed. Please check your API key and secret.")
                elif error_code == 403:
                    print("You are already authenticated.")
                elif error_code == 404:
                    print("Authentication timed out. Please reconnect and try again.")
                elif error_code == 405:
                    print("Symbol limit exceeded. Please check your subscription package.")
                elif error_code == 406:
                    print("Connection limit exceeded. You already have an ongoing authenticated session.")
                elif error_code == 407:
                    print("Slow client warning. Please improve your message processing speed.")
                elif error_code == 408:
                    print("Data v2 not enabled for your account.")
                elif error_code == 409:
                    print("Insufficient subscription. Please upgrade your subscription package.")
                elif error_code == 500:
                    print("Internal server error. Please try again later.")
                return
            
            # subscription confirmation for btc/usd pair
            if msg.get('T') == 'subscription':
                print("Subscription confirmation:")
                print(json.dumps(msg, indent=4))
                return
            
            # order boook updates
            if msg.get('T') == 'o':  # 'o' for orderbook
                symbol = msg.get('S')
                if symbol == 'BTC/USD':
                    self.last_update = time.strftime('%H:%M:%S')
                    
                    # updating the bids
                    for bid in msg.get('b', []):
                        bid_price = float(bid['p'])
                        bid_size = float(bid['s'])
                        if bid_size == 0:
                            self.bids.pop(bid_price, None)
                        else:
                            self.bids[bid_price] = bid_size
                    
                    # updating the asks
                    for ask in msg.get('a', []):
                        ask_price = float(ask['p'])
                        ask_size = float(ask['s'])
                        if ask_size == 0:
                            self.asks.pop(ask_price, None)
                        else:
                            self.asks[ask_price] = ask_size
                    
                    self.display_orderbook()
    
        else:
            print(f"Unexpected message format: {type(msg)} - {msg}")

# main function
async def main():
    orderbook = BTCOrderBookDisplay()
    await orderbook.connect()

# run the main func
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down orderbook display...")