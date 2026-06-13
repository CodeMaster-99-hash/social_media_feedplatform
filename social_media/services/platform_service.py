"""
Platform Service - Main service that coordinates all operations
This is the CORE of the social media platform!
"""
from typing import Optional, List
from social_media.models.user import User
from social_media.models.post import Post
from social_media.models.comment import Comment
from social_media.services.graph_service import UserGraph
from social_media.algorithms.feed_algorithm import FeedAlgorithm


class SocialMediaPlatform:
    """
    Main social media platform class.
    
    Coordinates all operations and manages all data.
    Everything goes through this class!
    """
    
    def __init__(self):
        """Initialize the platform with empty data."""
        self.users: dict = {}              # user_id → User
        self.posts: dict = {}              # post_id → Post
        self.graph = UserGraph()           # User relationships
        
        self.next_user_id = 1
        self.next_post_id = 1
        self.next_comment_id = 1
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, username: str, email: str, name: str = "") -> User:
        """
        Create a new user.
        
        Args:
            username: Unique username
            email: Email address
            name: Full name (optional)
            
        Returns:
            Created User object
            
        Raises:
            ValueError: If username already exists
        """
        # Check username uniqueness
        if any(u.username == username for u in self.users.values()):
            raise ValueError(f"Username '{username}' already taken!")
        
        user = User(self.next_user_id, username, email, name)
        self.users[self.next_user_id] = user
        self.next_user_id += 1
        
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID.
        O(1) operation!
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None if not found
        """
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by username.
        O(n) operation (must search all users).
        
        Args:
            username: Username
            
        Returns:
            User object or None
        """
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def follow_user(self, follower_id: int, following_id: int) -> bool:
        """
        Make one user follow another.
        
        Updates both user objects AND the graph.
        
        Args:
            follower_id: User who is following
            following_id: User being followed
            
        Returns:
            True if successful, False if already following
            
        Raises:
            ValueError: If users don't exist
        """
        if follower_id not in self.users:
            raise ValueError(f"User {follower_id} not found!")
        if following_id not in self.users:
            raise ValueError(f"User {following_id} not found!")
        
        follower = self.users[follower_id]
        following = self.users[following_id]
        
        # Update both user objects
        success = follower.follow_user(following_id)
        
        if success:
            # Update in both directions
            following.add_follower(follower_id)
            # Update graph
            self.graph.add_edge(follower_id, following_id)
        
        return success
    
    def unfollow_user(self, follower_id: int, following_id: int) -> bool:
        """
        Make one user unfollow another.
        
        Args:
            follower_id: User unfollowing
            following_id: User being unfollowed
            
        Returns:
            True if successful, False if not following
        """
        if follower_id not in self.users:
            raise ValueError(f"User {follower_id} not found!")
        if following_id not in self.users:
            raise ValueError(f"User {following_id} not found!")
        
        follower = self.users[follower_id]
        following = self.users[following_id]
        
        success = follower.unfollow_user(following_id)
        
        if success:
            following.remove_follower(follower_id)
            self.graph.remove_edge(follower_id, following_id)
        
        return success
    
    # ==================== POST OPERATIONS ====================
    
    def create_post(self, user_id: int, content: str) -> Post:
        """
        Create a new post.
        
        Args:
            user_id: ID of post creator
            content: Post content
            
        Returns:
            Created Post object
            
        Raises:
            ValueError: If user doesn't exist or content invalid
        """
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found!")
        
        post = Post(self.next_post_id, user_id, content)
        self.posts[self.next_post_id] = post
        
        # Add post to user
        user = self.users[user_id]
        user.add_post(self.next_post_id)
        
        self.next_post_id += 1
        return post
    
    def get_post(self, post_id: int) -> Optional[Post]:
        """
        Get a post by ID.
        O(1) operation!
        
        Args:
            post_id: Post ID
            
        Returns:
            Post object or None
        """
        return self.posts.get(post_id)
    
    def like_post(self, user_id: int, post_id: int) -> bool:
        """
        Like a post.
        O(1) operation!
        
        Args:
            user_id: User liking the post
            post_id: Post being liked
            
        Returns:
            True if liked, False if already liked
        """
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found!")
        if post_id not in self.posts:
            raise ValueError(f"Post {post_id} not found!")
        
        post = self.posts[post_id]
        return post.add_like(user_id)
    
    def unlike_post(self, user_id: int, post_id: int) -> bool:
        """
        Unlike a post.
        O(1) operation!
        
        Args:
            user_id: User unliking
            post_id: Post being unliked
            
        Returns:
            True if unliked, False if not liked
        """
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found!")
        if post_id not in self.posts:
            raise ValueError(f"Post {post_id} not found!")
        
        post = self.posts[post_id]
        return post.remove_like(user_id)
    
    # ==================== COMMENT OPERATIONS ====================
    
    def add_comment(
        self, 
        user_id: int, 
        post_id: int, 
        content: str
    ) -> Comment:
        """
        Add a comment to a post.
        
        Args:
            user_id: User making comment
            post_id: Post being commented on
            content: Comment text
            
        Returns:
            Created Comment object
        """
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found!")
        if post_id not in self.posts:
            raise ValueError(f"Post {post_id} not found!")
        
        comment = Comment(self.next_comment_id, post_id, user_id, content)
        post = self.posts[post_id]
        post.add_comment(comment)
        
        self.next_comment_id += 1
        return comment
    
    # ==================== FEED OPERATIONS ====================
    
    def get_user_feed(self, user_id: int, limit: int = 10) -> List[Post]:
        """
        Get the feed for a user.
        
        THIS IS THE MAIN FEATURE OF THE PROJECT!
        
        Time Complexity: O(n log n) where n = total posts from following
        
        Algorithm:
        1. Get list of users this person follows
        2. Collect all posts from those users
        3. Use Feed Algorithm to rank by engagement
        4. Return top posts
        
        Args:
            user_id: User requesting feed
            limit: Number of posts to return
            
        Returns:
            List of top ranked posts for user's feed
        """
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found!")
        
        user = self.users[user_id]
        following_list = user.following
        
        # Get all posts from followed users
        user_posts_dict = {}
        for followed_id in following_list:
            if followed_id in self.users:
                followed_user = self.users[followed_id]
                user_posts_dict[followed_id] = [
                    self.posts[post_id] 
                    for post_id in followed_user.get_posts()
                    if post_id in self.posts
                ]
        
        # Generate feed using algorithm
        feed = FeedAlgorithm.generate_feed(
            user_id,
            following_list,
            user_posts_dict,
            limit=limit
        )
        
        return feed
    
    def get_personalized_feed(self, user_id: int, limit: int = 10) -> List[Post]:
        """
        Get a more personalized feed.
        
        Improvements:
        - Don't show posts user already liked
        - Diversify posts (limit same user)
        
        Args:
            user_id: User requesting feed
            limit: Number of posts
            
        Returns:
            Personalized ranked posts
        """
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found!")
        
        user = self.users[user_id]
        following_list = user.following
        
        # Get liked post IDs
        liked_posts = set()
        for post in self.posts.values():
            if post.has_liked(user_id):
                liked_posts.add(post.post_id)
        
        # Build user posts dict
        user_posts_dict = {}
        for followed_id in following_list:
            if followed_id in self.users:
                followed_user = self.users[followed_id]
                user_posts_dict[followed_id] = [
                    self.posts[post_id]
                    for post_id in followed_user.get_posts()
                    if post_id in self.posts
                ]
        
        # Generate personalized feed
        feed = FeedAlgorithm.generate_personalized_feed(
            user_id,
            following_list,
            user_posts_dict,
            liked_posts,
            limit=limit
        )
        
        return feed
    
    # ==================== GRAPH OPERATIONS ====================
    
    def suggest_friends(self, user_id: int, limit: int = 5) -> List[User]:
        """
        Suggest friends for a user (friends of friends).
        
        Uses Graph Service and BFS algorithm.
        
        Args:
            user_id: User requesting suggestions
            limit: Number of suggestions
            
        Returns:
            List of suggested User objects
        """
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found!")
        
        suggested_ids = self.graph.suggest_friends(user_id, limit)
        return [self.users[uid] for uid in suggested_ids if uid in self.users]
    
    def get_mutual_friends(self, user_a_id: int, user_b_id: int) -> List[User]:
        """
        Get mutual friends between two users.
        
        Args:
            user_a_id: First user
            user_b_id: Second user
            
        Returns:
            List of mutual User objects
        """
        if user_a_id not in self.users:
            raise ValueError(f"User {user_a_id} not found!")
        if user_b_id not in self.users:
            raise ValueError(f"User {user_b_id} not found!")
        
        mutual_ids = self.graph.find_mutual_friends(user_a_id, user_b_id)
        return [self.users[uid] for uid in mutual_ids if uid in self.users]
    
    # ==================== STATISTICS ====================
    
    def get_platform_stats(self) -> dict:
        """
        Get overall platform statistics.
        
        Returns:
            Dictionary with platform metrics
        """
        total_likes = sum(post.get_like_count() for post in self.posts.values())
        total_comments = sum(post.get_comment_count() for post in self.posts.values())
        
        return {
            'total_users': len(self.users),
            'total_posts': len(self.posts),
            'total_likes': total_likes,
            'total_comments': total_comments,
            'avg_followers': sum(u.get_follower_count() for u in self.users.values()) / max(len(self.users), 1)
        }