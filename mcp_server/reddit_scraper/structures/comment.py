class Comment:
    def __init__(self, id: str, author: str, upvotes: int, downvotes: int, body: str, sub: str):
        self.id = id
        self.author = author 
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.body = body
        self.sub = sub

    def format_comment_str(self) -> str:
        return f"""
id: {self.id}
author: {self.author}
comment: {self.body}
upvotes: {str(self.upvotes)}
downvotes: {str(self.downvotes)}
subreddit: {self.sub}
"""