import httpx
from httpx import BasicAuth, RequestError
import asyncio
from dotenv import load_dotenv
import os
from reddit_scraper.structures.post import Post
from reddit_scraper.structures.comment import Comment

load_dotenv()

class Scraper:
    authURL = "https://www.reddit.com/api/v1/access_token"
    baseURL = "https://oauth.reddit.com"
    access_token = ""

    def __init__(self, id: str):
        self.id = id
        self.status = "INITIALIZED"
    
    # recive access token and authorize the client
    @classmethod
    async def generate_token(cls):

        async with httpx.AsyncClient() as client:
            basicAuth = BasicAuth(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
            form_data = {
                "grant_type": "password",
                "username": str(os.getenv("USERNAME")),
                "password" : str(os.getenv("PASSWORD"))
             }
            try:
                response = await client.post(cls.authURL, auth=basicAuth, data=form_data)

                if response.status_code != 200:
                    print("Token not granted")
                    raise RequestError
                
                data = response.json()
                access_token = data["access_token"]
                print("token granted successfully")
                cls.access_token = access_token

            except RequestError as e:
                print(f"Error fetching token: {e}")
    
    # fetches top posts from a mentioned subreddit
    async def fetch_posts(self, sub: str,  sort: str = "top", limit: int = 15) -> list[Post] | str:
        async with httpx.AsyncClient() as client:
            userHeaders = {
                "User-Agent": f"Python:simple-scraper:v1.0 (by /u/{os.getenv("USERNAME")})",
                "Authorization" : f"Bearer {Scraper.access_token}"
            }
            try:
                response = await client.get(f"{Scraper.baseURL}/r/{sub}/{sort}?limit={limit}", headers=userHeaders)

                if response.status_code != 200:
                    print("Problem fetching posts")
                    raise RequestError("Error fetching the posts")
                
                data = response.json()

                responsePosts = data["data"]["children"]

                posts = []

                for post in responsePosts:
                    # print(f"content:\n{post["data"]["selftext"]}")
                    # print("==============================\n\n")
                    postData = post["data"]
                    id, title, content, upvotes, downvotes, url = postData["id"], postData["title"], postData["selftext"], postData["score"], postData["downs"], postData["url"]
                    posts.append(Post(id, title, content, upvotes, downvotes, url))

                return posts

            except RequestError as e:
                import traceback
                print(f"Error fetching posts: {e}")
                traceback.print_exc()
                return str(e)

    async def fetch_post_comments(self, sub: str, post_id: str, limit: int = 20) -> list[Comment]:
        try:
            async with httpx.AsyncClient() as client:
                userHeaders = {
                    "User-Agent": f"Python:simple-scraper:v1.0 (by /u/{os.getenv("USERNAME")})",
                    "Authorization" : f"Bearer {Scraper.access_token}"
                }

                url = f"{Scraper.baseURL}/r/{str(sub)}/comments/{post_id}?limit={limit}"
                print(url)
                response = await client.get(url=url, headers=userHeaders)

                if response.status_code != 200:
                    raise RequestError(f"Request status not OK: {response.status_code}")
                
                data = response.json()
                comment_res = data.pop()["data"]["children"]

                comments = [ Comment(id=comment["data"]["id"], author=comment["data"]["author"], body=comment["data"]["body"], upvotes=comment["data"]["score"], downvotes=comment["data"]["downs"],sub=comment["data"]["subreddit"]) for comment in comment_res]

                return comments
            
        except Exception as e:
            import traceback
            print(f"Error fetching comments: {e}")
            traceback.print_exc()
            return str(e)









# async def main():
#     try:
#         scraper = Scraper("123")
#         print(scraper.status)
#         await Scraper.generate_token()
#         comments: list[Comment] = await scraper.fetch_post_comments("python", "1lhbsgi")
#         for comment in comments:
#             print(comment.format_comment_str())
#             print("\n===========================\n")
#     except Exception as e:
#         print(f"Some error occured:\n{e}")
     
# if __name__ == "__main__":
#     asyncio.run(main())