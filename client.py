import time
import hmac
import hashlib
import requests

class BinanceTestnetClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com" 
    def _generate_signature(self, query_string: str) -> str:
        """Signs the request payload using HMAC SHA256."""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def send_signed_request(self, method: str, endpoint: str, params: dict = None) -> dict:
        """Sends a secured, timestamped request to Binance Futures Testnet."""
        if params is None:
            params = {}
            
        
        params['timestamp'] = int(time.time() * 1000)
        
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = self._generate_signature(query_string)
        query_string += f"&signature={signature}"
        
        url = f"{self.base_url}{endpoint}?{query_string}"
        headers = {"X-MBX-APIKEY": self.api_key}
        
        response = requests.request(method, url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Binance API Error {response.status_code}: {response.text}")
            
        return response.json()