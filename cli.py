import sys
import os
import argparse
import logging


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from logging_config import setup_logging
from client import BinanceTestnetClient
from validators import validate_inputs
from orders import OrderManager


API_KEY = "BvAQrIGX8ruPIQxDnUasA3jK8O7XJDuem4byU5z8MFOs477wtI2q8IdrQiTJyRY0"
API_SECRET = "zya1sKkEEse8PKvJG2PNEDHY0ByxOfMPXkjLutlyzZ8N7jDboACBEju3iInaFnug"

def render_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("┌────────────────────────────────────────────────────────┐")
    print("│         PRIMETRADE.AI — ADVANCED BOT ENGINE            │")
    print("│         [STATUS: CONNECTED TO FUTURES TESTNET]         │")
    print("└────────────────────────────────────────────────────────┘")

def launch_interactive_wizard():
    render_header()
    print("\n[STEP 1] Enter Target Asset Pair")
    print("────────────────────────────────────────────────────────")
    symbol = input("  ▸ Symbol (e.g., BTCUSDT): ").strip().upper()
    if not symbol: symbol = "BTCUSDT"

    render_header()
    print(f"\n[STEP 2] Select Execution Side for {symbol}")
    print("────────────────────────────────────────────────────────")
    print("  [1] 🟢 BUY  (Go Long)")
    print("  [2] 🔴 SELL (Go Short)")
    print("────────────────────────────────────────────────────────")
    side_choice = input("  ▸ Select Option (1 or 2): ").strip()
    side = "SELL" if side_choice == "2" else "BUY"

    render_header()
    print(f"\n[STEP 3] Select Order Constraints Structure")
    print("────────────────────────────────────────────────────────")
    print("  [1] ⚡ MARKET (Immediate Execution at Orderbook Price)")
    print("  [2] 🎯 LIMIT  (Resting Order at Specified Price Target)")
    print("────────────────────────────────────────────────────────")
    type_choice = input("  ▸ Select Option (1 or 2): ").strip()
    order_type = "LIMIT" if type_choice == "2" else "MARKET"

    render_header()
    print(f"\n[STEP 4] Specify Transaction Size")
    print("────────────────────────────────────────────────────────")
    try:
        quantity = float(input(f"  ▸ Enter Quantity in Contracts: ").strip())
    except ValueError:
        quantity = 0.0

    price = None
    if order_type == "LIMIT":
        render_header()
        print(f"\n[STEP 5] Set Target Pricing Parameters")
        print("────────────────────────────────────────────────────────")
        try:
            price = float(input("  ▸ Enter Limit Execution Price: ").strip())
        except ValueError:
            price = 0.0

    return symbol, side, order_type, quantity, price

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description="🚀 Binance Futures Testnet Advanced Trading Bot")
    parser.add_argument("--symbol", help="Trading pair")
    parser.add_argument("--side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", choices=["MARKET", "LIMIT"], help="Order type")
    parser.add_argument("--quantity", type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Order price")
    
    args = parser.parse_args()
    
    if not any([args.symbol, args.side, args.type, args.quantity, args.price]):
        symbol, side, order_type, quantity, price = launch_interactive_wizard()
    else:
        symbol, side, order_type, quantity, price = args.symbol, args.side, args.type, args.quantity, args.price
    
    render_header()
    print("\n⚡ PIPELINE TRACKING")
    print("────────────────────────────────────────────────────────")
    
    try:
        validate_inputs(symbol, side, order_type, quantity, price)
        print("  ✔ SUCCESS: Parameter validation boundaries clear.")
        print("  ✔ NETWORK: Encoding signed SHA256 HMAC payload...")
        
        logging.info(f"Initiating Order Request: {side} {quantity} {symbol} Type: {order_type}")
        
        client = BinanceTestnetClient(API_KEY, API_SECRET)
        manager = OrderManager(client)
        
        response = manager.execute_order(
            symbol=symbol, side=side, order_type=order_type, quantity=quantity, price=price
        )
        
        order_id = response.get("orderId", "N/A")
        status = response.get("status", "N/A")
        exec_qty = response.get("executedQty", "N/A")
        avg_price = response.get("avgPrice", "N/A")
        
        logging.info(f"SUCCESS: Order executed successfully.")
        
        print("\n┌────────────────────────────────────────────────────────┐")
        print("│ 🎉 TELEMETRY SUCCESS: ORDER PLACED ON TESTNET         │")
        print("├────────────────────────────────────────────────────────┤")
        print(f"│  • Order Identification ID : {str(order_id).ljust(26)} │")
        print(f"│  • Engine Lifecycle Status : {str(status).ljust(26)} │")
        print(f"│  • Total Executed Volume   : {str(exec_qty).ljust(26)} │")
        print(f"│  • Asset Execution Average : {str(avg_price).ljust(26)} │")
        print("└────────────────────────────────────────────────────────┘\n")
        
    except ValueError as val_err:
        logging.error(f"Validation Failure: {str(val_err)}")
        print("\n┌────────────────────────────────────────────────────────┐")
        print("│ ❌ INTERCEPTED PIPELINE CRITICAL RUNTIME FAULT          │")
        print("├────────────────────────────────────────────────────────┤")
        print(f"│ {str(val_err).ljust(54)} │")
        print("└────────────────────────────────────────────────────────┘\n")
        
    except Exception as api_err:
        logging.error(f"Execution Error: {str(api_err)}")
        print("\n┌────────────────────────────────────────────────────────┐")
        print("│ ❌ CRITICAL BINANCE GATEWAY REJECTION ENCOUNTERED      │")
        print("├────────────────────────────────────────────────────────┤")
        print(f"│ {str(api_err)[:52].ljust(54)} │")
        print("└────────────────────────────────────────────────────────┘\n")

if __name__ == "__main__":
    main()