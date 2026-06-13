"""
User Model - Represents a user in the social media platform
"""
from datetime import datetime
from typing import Set, List


class User:
    """
    Represents a user in the social media platform.
    
    Attributes:
        user_id (int): Unique identifier for the user
        username (str): User's username
        email (str): User's email address
        name (str): User's full name
        bio (str): User's bio/description
        followers (Set[int]): Set of user IDs who follow this user
        following (Set[int]): Set of user IDs this user follows
        posts (List[int]): List of post IDs created by this user
        created_at (datetime): When the user account was created
    """
    
    def __init__(self, user_id: int, username: str, email: str, name: str = ""):
        """
        Initialize a new user.
        
        Args:
            user_id: Unique identifier
            username: Username
            email: Email address
            name: Full name (optional)
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.name = name
        self.bio = ""
        
        # Use SET for O(1) lookup performance
        # DONT use List! That's O(n)
        # DO use Set! That's O(1)
        self.followers: Set[int] = set()      # Who follows me
        self.following: Set[int] = set()      # I follow
        self.posts: List[int] = []            # My posts (ordered)
        
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def follow_user(self, other_user_id: int) -> bool:
        """
        Follow another user.
        
        Args:
            other_user_id: ID of user to follow
            
        Returns:
            True if successfully followed, False if already following
            
        Raises:
            ValueError: If trying to follow yourself
        """
        # Can't follow yourself!
        if other_user_id == self.user_id:
            raise ValueError("Cannot follow yourself!")
        
        # Already following? Return False
        if other_user_id in self.following:
            return False  # Already following
        
        # Add to following set (O(1) operation!)
        self.following.add(other_user_id)
        self.updated_at = datetime.now()
        return True
    
    def unfollow_user(self, other_user_id: int) -> bool:
        """
        Unfollow another user.
        
        Args:
            other_user_id: ID of user to unfollow
            
        Returns:
            True if successfully unfollowed, False if not following
        """
        # Not following? Return False
        if other_user_id not in self.following:
            return False
        
        # Remove from following set (O(1) operation!)
        self.following.discard(other_user_id)
        self.updated_at = datetime.now()
        return True
    
    def add_follower(self, follower_id: int) -> bool:
        """
        Add a follower (called when someone follows this user).
        
        Args:
            follower_id: ID of new follower
            
        Returns:
            True if added, False if already following
        """
        if follower_id in self.followers:
            return False
        
        self.followers.add(follower_id)
        self.updated_at = datetime.now()
        return True
    
    def remove_follower(self, follower_id: int) -> bool:
        """
        Remove a follower.
        
        Args:
            follower_id: ID of follower to remove
            
        Returns:
            True if removed, False if not a follower
        """
        if follower_id not in self.followers:
            return False
        
        self.followers.discard(follower_id)
        self.updated_at = datetime.now()
        return True
    
    def get_follower_count(self) -> int:
        """
        Get number of followers. O(1) operation!
        """
        return len(self.followers)
    
    def get_following_count(self) -> int:
        """
        Get number of users this user follows. O(1) operation!
        """
        return len(self.following)
    
    def is_following(self, other_user_id: int) -> bool:
        """
        Check if following a user. O(1) operation!
        
        This is why we use SET instead of LIST.
        With List: must check each item - O(n)
        With Set: instant lookup - O(1)
        """
        return other_user_id in self.following
    
    def is_follower(self, other_user_id: int) -> bool:
        """
        Check if user is a follower. O(1) operation!
        """
        return other_user_id in self.followers
    
    def get_posts(self) -> List[int]:
        """
        Get list of post IDs created by this user.
        """
        return self.posts.copy()  # Return copy for safety
    
    def add_post(self, post_id: int) -> None:
        """
        Add a post ID to this user's posts.
        """
        self.posts.append(post_id)
        self.updated_at = datetime.now()
    
    def __repr__(self) -> str:
        """
        String representation of user.
        Used when you print(user) or str(user)
        """
        return (f"User(id={self.user_id}, username='{self.username}', "
                f"followers={self.get_follower_count()}, "
                f"following={self.get_following_count()})")
    
    def to_dict(self) -> dict:
        """
        Convert user to dictionary.
        Useful for returning JSON or debugging.
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'bio': self.bio,
            'followers_count': self.get_follower_count(),
            'following_count': self.get_following_count(),
            'posts_count': len(self.posts),
            'created_at': self.created_at.isoformat()
        }
