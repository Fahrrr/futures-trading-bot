def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """Validates user input fields before firing API requests."""
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Invalid symbol. Must be a non-empty string (e.g., 'BTCUSDT').")
        
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Invalid side. Must be either 'BUY' or 'SELL'.")
        
    if order_type.upper() not in ["MARKET", "LIMIT"]:
        raise ValueError("Invalid order type. Must be either 'MARKET' or 'LIMIT'.")
        
    if quantity <= 0:
        raise ValueError("Quantity must be a positive number greater than zero.")
        
    if order_type.upper() == "LIMIT" and (price is None or price <= 0):
        raise ValueError("A positive price is strictly required for LIMIT orders.")