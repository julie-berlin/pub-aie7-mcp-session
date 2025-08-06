from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dice_roller import DiceRoller
from exchange_rates import ExchangeRateClient

load_dotenv()

mcp = FastMCP("local-mcp-server")
web_search_client = TavilyClient(os.getenv("TAVILY_API_KEY"))
exchange_rate_client = ExchangeRateClient(os.getenv("EXCHANGERATE_API_KEY"))

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    search_results = web_search_client.get_search_context(query=query)
    return search_results

@mcp.tool()
def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation"""
    roller = DiceRoller(notation, num_rolls)
    return str(roller)

"""
Add your own tool here, and then use it through Cursor!
"""
@mcp.tool()
async def get_exchange_rate(currency_code: str) -> str:
    """Get the latest exchange rates from provided base currency code (ISO 4217) to all other supported currencies"""
    exchange_rates = exchange_rate_client.get_rates(code=currency_code)
    return exchange_rates

if __name__ == "__main__":
    mcp.run(transport="stdio")
