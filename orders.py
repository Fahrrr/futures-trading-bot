from client import BinanceTestnetClient

class OrderManager:
    def __init__(self, client: BinanceTestnetClient):
        self.client = client

    def execute_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
        """Constructs the exact parameters needed to open a long or short position."""
        endpoint = "/fapi/v1/order"
        
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
        }
        
        
        if order_type.upper() == "LIMIT":
            if not price:
                raise ValueError("Price is mandatory for LIMIT orders.")
            params["price"] = price
            params["timeInForce"] = "GTC" 
            
        return self.client.send_signed_request("POST", endpoint, params)    