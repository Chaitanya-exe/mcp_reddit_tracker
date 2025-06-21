class Post:
    def __init__(self, id: str, title: str, content: str, upvotes: int, downvotes: int):
        self.id = id
        self.title = title
        self.content = content
        self.upvotes = upvotes
        self.downvotes = downvotes

    def format_post_str(self):
        return f"""
id: {self.id}
title: {self.title}
content: {self.content}
upvotes: {str(self.upvotes)}
downvotes: {str(self.downvotes)}
"""
    
