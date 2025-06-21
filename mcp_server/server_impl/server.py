from mcp.server.fastmcp import FastMCP
from typing import Any
from reddit_scraper.scraper import Scraper
from reddit_scraper.post import Post

class MCPServer:
    
    def __init__(self,namespace: str, transport: str, scraper: Scraper):
        self.mcp = FastMCP(namespace, debug=True)
        self.transport = transport
        self.scraper = scraper

        # tool registerations
        self.mcp.tool(
            name="get_posts_from_sub",
            description="Fetch top posts from a specified subreddit",
        )(self.get_posts_from_sub)

    def run(self):
        print("server initialized and running...")
        self.mcp.run(transport=self.transport)

    async def get_posts_from_sub(self, sub: str) -> str:
        """
        Fetch top posts from a specified subreddit.

        Args:
            sub: Name of the subreddit to fetch posts from.

        Returns:
            Formatted list of top posts.
        """

        try:
            posts = await self.scraper.fetch_posts(sub)
            postStr = []

            for post in posts:
                postStr.append(post.format_post_str())
            
            print("Tool was called\n")
            return "\n---\n".join(postStr)
        except Exception as e:
            import traceback
            print(f"some error occured: {e}")
            traceback.print_exc()
            return str(e)



        