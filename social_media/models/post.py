"""
Post Model - Represents a post on the social media platform
"""
from datetime import datetime
from typing import Set, List


class Post:
    """
    Represents a post on the social media platform.
    
    Attributes:
        post_id (int): Unique identifier for the post
        user_id (int): ID of the user who created the post
        content (str): The post content/text
        likes (Set[int]): Set of user IDs who liked this post
        comments (List[Comment]): List of comments on this post
        timestamp (datetime): When the post was created
    """
    
    def __init__(self, post_id: int, user_id: int, content: str):
        """
        Initialize a new post.
        
        Args:
            post_id: Unique identifier
            user_id: ID of creator
            content: Post content
            
        Raises:
            ValueError: If content is empty or too long
        """
        # Validate content
        if not content or len(content) == 0:
            raise ValueError("Post content cannot be empty!")
        
        if len(content) > 10000:
            raise ValueError("Post content too long (max 10000 chars)!")
        
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        
        # Use SET for O(1) like/unlike operations
        # DONT use List! That's O(n)
        # DO use Set! That's O(1)
        self.likes: Set[int] = set()
        self.comments: List['Comment'] = []
        
        self.timestamp = datetime.now()
        self.updated_at = datetime.now()
    
    def add_like(self, user_id: int) -> bool:
        """
        Add a like from a user. O(1) operation!
        
        Args:
            user_id: ID of user liking the post
            
        Returns:
            True if liked, False if already liked
        """
        # Check if already liked
        if user_id in self.likes:
            return False  # Already liked
        
        # Add to likes set (O(1) operation!)
        self.likes.add(user_id)
        self.updated_at = datetime.now()
        return True
    
    def remove_like(self, user_id: int) -> bool:
        """
        Remove a like from a user. O(1) operation!
        
        Args:
            user_id: ID of user unliking the post
            
        Returns:
            True if removed, False if not liked
        """
        # Check if liked
        if user_id not in self.likes:
            return False
        
        # Remove from likes set (O(1) operation!)
        self.likes.discard(user_id)
        self.updated_at = datetime.now()
        return True
    
    def has_liked(self, user_id: int) -> bool:
        """
        Check if user liked this post. O(1) operation!
        
        Args:
            user_id: User ID
            
        Returns:
            True if user liked post
        """
        return user_id in self.likes
    
    def get_like_count(self) -> int:
        """
        Get number of likes. O(1) operation.
        
        Returns:
            Number of likes
        """
        return len(self.likes)
    
    def add_comment(self, comment: 'Comment') -> None:
        """
        Add a comment to this post.
        
        Args:
            comment: Comment object
        """
        self.comments.append(comment)
        self.updated_at = datetime.now()
    
    def get_comment_count(self) -> int:
        """
        Get number of comments.
        
        Returns:
            Number of comments
        """
        return len(self.comments)
    
    def get_comments(self) -> List['Comment']:
        """
        Get list of comments.
        
        Returns:
            Copy of comments list
        """
        return self.comments.copy()
    
    def get_engagement_score(self) -> float:
        """
        Calculate engagement score for ranking in feed.
        
        Formula: (likes * 2) + (comments * 3)
        
        This is what we SORT BY to create the feed!
        Posts with higher scores appear first.
        
        Examples:
        - 10 likes, 2 comments: (10*2) + (2*3) = 26
        - 20 likes, 5 comments: (20*2) + (5*3) = 55
        - 5 likes, 10 comments: (5*2) + (10*3) = 40
        
        Returns:
            Float representing engagement score
        """
        like_score = self.get_like_count() * 2
        comment_score = self.get_comment_count() * 3
        
        return float(like_score + comment_score)
    
    def get_age_minutes(self) -> float:
        """
        Get post age in minutes.
        
        Returns:
            How many minutes old the post is
        """
        return (datetime.now() - self.timestamp).total_seconds() / 60
    
    def __repr__(self) -> str:
        """
        String representation of post.
        Used when you print(post) or str(post)
        """
        return (f"Post(id={self.post_id}, user_id={self.user_id}, "
                f"likes={self.get_like_count()}, "
                f"comments={self.get_comment_count()})")
    
    def to_dict(self) -> dict:
        """
        Convert post to dictionary.
        Useful for returning JSON or debugging.
        
        Returns:
            Dictionary representation of post
        """
        return {
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content,
            'likes_count': self.get_like_count(),
            'comments_count': self.get_comment_count(),
            'engagement_score': self.get_engagement_score(),
            'timestamp': self.timestamp.isoformat()
        }