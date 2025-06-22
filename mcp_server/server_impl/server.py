from mcp.server.fastmcp import FastMCP
from typing import Any
from reddit_scraper.scraper import Scraper
from reddit_scraper.post import Post
from nltk import word_tokenize
from nltk.probability import FreqDist

class MCPServer:

    # constructor method
    def __init__(self,namespace: str, transport: str, scraper: Scraper):
        self.mcp = FastMCP(namespace, debug=True)
        self.transport = transport
        self.scraper = scraper

        # tool registerations
        self.mcp.tool(
            name="get_posts_from_sub",
            description="Fetch top posts from a specified subreddit",
        )(self.get_posts_from_sub)
        self.mcp.tool(
            name="extract_keywords",
            description="Extracts trending keywords from the provided posts"
        )(self.extract_keywords)

    # main running server method
    def run(self):
        print("server initialized and running...")
        self.mcp.run(transport=self.transport)

    # tool 1 to fetch posts from subreddit
    async def get_posts_from_sub(self, sub: str, sort: str = "top", limit: int = 10) -> str:
        """
    Fetches a list of top posts from a specified subreddit using the Reddit API.

    This tool retrieves a specified number of posts from a given subreddit, using a configurable sorting method such as
    "top", "hot", "new", etc. The response includes post titles and metadata, formatted into a human-readable string.

    Args:
        sub (str): The name of the subreddit to query (without the "r/" prefix).
        sort (str, optional): The sorting method to apply when fetching posts.
            Must be one of: 'top', 'hot', 'new', 'best', 'controversial', or 'rising'.
            Defaults to 'top'.
        limit (int, optional): The number of posts to retrieve. Defaults to 10.

    Returns:
        str: A formatted string containing the list of fetched posts with their titles and relevant metadata.

    Note:
        - Subreddit names are case-insensitive.
        - Results depend on Reddit’s public API rate limits and availability.
    """

        try:

            # check for prefix and extract name correctly to prevent Bad Request
            if len(sub.split("/")) > 1:
                sub = sub.split("/").pop()
            
            # fetch post request and type checking of result
                if sort is None or limit is None:
                    sort = "top"
                    limit = 10
                
            posts = await self.scraper.fetch_posts(sub, str(sort), int(limit))
            if posts is list[Post]:
                return "Error occured while fetching posts"
            
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

    # tool 2 to extract keywords from the content
    async def extract_keywords(self, sub: str, n: int = 10) -> str:
        """
    Extracts the most frequent keywords from the top recent posts in a specified subreddit.

    This tool fetches a collection of recent posts from the given subreddit, processes the text content (titles and bodies),
    and performs keyword extraction by identifying the most frequently occurring alphanumeric words. It returns a
    ranked list of the top `n` keywords based on their frequency of appearance.

    Args:
        sub (str): The name of the subreddit (e.g., "technology") to analyze.
        n (int, optional): The number of top keywords to extract. Defaults to 10.

    Returns:
        str: A formatted string listing the top `n` keywords along with their respective frequencies,
            sorted in descending order of occurrence.

    Note:
        - Common stopwords are not removed in this basic implementation.
        - Only alphanumeric tokens are considered for keyword extraction.
    """

        try:

            # fetch post
            if len(sub.split("/")) > 1:
                sub = sub.split("/").pop()
            
            # fetch posts and generating combined text
            posts = await self.scraper.fetch_posts(sub)
            combined_text = " ".join([post.title + " " + post.content for post in posts])

            # tokenization of words 
            tokens = word_tokenize(combined_text.lower())
            words = [word for word in tokens if word.isalnum()]

            # frequency counter to filter keywords
            freq_dist = FreqDist(words)
            top_keywords = freq_dist.most_common(n)

            return "\n".join([f"{word}: {count}" for word, count in top_keywords])

        except Exception as e:
            import traceback
            print(f"some error occured: {e}")
            traceback.print_exc()
            return str(e)
        pass


        