import requests
import json


class ExchangeRateClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://v6.exchangerate-api.com/v6"
    
    def get_rates(self, code: str) -> str:
        """Get latest exchange rates for the specified base currency code"""
        if not self.api_key:
            raise ValueError("API key is required")
        
        url = f"{self.base_url}/{self.api_key}/latest/{code.upper()}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("result") == "success":
                rates = data.get("conversion_rates", {})
                base_code = data.get("base_code")
                last_update = data.get("time_last_update_utc")
                
                result = {
                    "base_currency": base_code,
                    "last_updated": last_update,
                    "exchange_rates": rates
                }
                
                return json.dumps(result, indent=2)
            else:
                error_type = data.get("error-type", "unknown")
                return f"Error: {error_type}"
                
        except requests.exceptions.RequestException as e:
            return f"Network error: {str(e)}"
        except json.JSONDecodeError:
            return "Error: Invalid response format"
        except Exception as e:
            return f"Unexpected error: {str(e)}"