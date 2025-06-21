import asyncio
from reddit_scraper.scraper import Scraper
from server_impl.server import MCPServer

# async def main():
#     scraper = Scraper("123")
#     await Scraper.generate_token()
#     server = MCPServer("trend_tracker_mcp_server", "stdio", scraper)
#     server.run()

if __name__ == "__main__":
    try:
        scraper = Scraper("123")
        asyncio.run(Scraper.generate_token())
        server = MCPServer("trend_tracker_mcp_server", "stdio", scraper)
        server.run()
    except KeyboardInterrupt as e:
        print(f"Shutting down server... {e}")