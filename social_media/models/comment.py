"""
Comment Model - Represents a comment on a post
"""
from datetime import datetime


class Comment:
    """
    Represents a comment on a post.
    
    A comment is a reply/response to a post.
    
    Attributes:
        comment_id (int): Unique identifier for the comment
        post_id (int): ID of the post being commented on
        user_id (int): ID of the user making the comment
        content (str): Comment text content
        timestamp (datetime): When comment was created
    """
    
    def __init__(self, comment_id: int, post_id: int, user_id: int, content: str):
        """
        Initialize a new comment.
        
        Args:
            comment_id: Unique identifier
            post_id: ID of post
            user_id: ID of commenter
            content: Comment text
            
        Raises:
            ValueError: If content is empty or too long
        """
        # Validate content
        if not content or len(content) == 0:
            raise ValueError("Comment cannot be empty!")
        
        if len(content) > 5000:
            raise ValueError("Comment too long (max 5000 chars)!")
        
        self.comment_id = comment_id
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.timestamp = datetime.now()
    
    def __repr__(self) -> str:
        """
        String representation of comment.
        Used when you print(comment) or str(comment)
        """
        return f"Comment(id={self.comment_id}, user_id={self.user_id})"
    
    def to_dict(self) -> dict:
        """
        Convert comment to dictionary.
        Useful for returning JSON or debugging.
        
        Returns:
            Dictionary representation of comment
        """
        return {
            'comment_id': self.comment_id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }