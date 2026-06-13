"""
Feed Algorithm - Generates and ranks user feeds
"""
from typing import List, Dict
from datetime import datetime, timedelta


class FeedAlgorithm:
    """
    Algorithm for generating and ranking feeds.
    
    The feed is the main feature of social media!
    Users see posts ranked by engagement.
    """
    
    @staticmethod
    def calculate_engagement_score(
        likes: int,
        comments: int,
        shares: int = 0,
        hours_old: float = 0
    ) -> float:
        """
        Calculate engagement score for ranking posts.
        
        Weights:
        - Likes: 2 points each
        - Comments: 3 points each (more valuable)
        - Shares: 5 points each (most valuable)
        - Freshness: Recent posts slightly boosted
        
        Formula: (likes * 2) + (comments * 3) + (shares * 5) * freshness_factor
        
        Examples:
        - 10 likes, 2 comments = (10*2) + (2*3) = 26
        - 20 likes, 5 comments = (20*2) + (5*3) = 55
        - 5 likes, 10 comments = (5*2) + (10*3) = 40
        
        Args:
            likes: Number of likes
            comments: Number of comments
            shares: Number of shares
            hours_old: How many hours old the post is
            
        Returns:
            Float score for ranking
        """
        # Base engagement score
        score = (likes * 2) + (comments * 3) + (shares * 5)
        
        # Slight freshness boost (but don't penalize old posts too much)
        freshness_factor = 1.0
        if hours_old < 24:  # First day boost
            freshness_factor = 1.1
        elif hours_old < 7 * 24:  # Week boost
            freshness_factor = 1.05
        
        return score * freshness_factor
    
    @staticmethod
    def rank_posts_by_engagement(posts: List) -> List:
        """
        Sort posts by engagement score (most engaging first).
        
        Uses Python's Timsort: O(n log n)
        
        Timsort:
        - Hybrid of merge sort and insertion sort
        - Optimal for real-world data
        - Very efficient
        
        Args:
            posts: List of Post objects
            
        Returns:
            Sorted list of posts (highest engagement first)
        """
        # Sort by engagement score descending (highest first)
        # sorted() uses Timsort - O(n log n)
        # reverse=True means highest scores first
        return sorted(
            posts,
            key=lambda post: post.get_engagement_score(),
            reverse=True
        )
    
    @staticmethod
    def generate_feed(
        user_id: int,
        following_list: set,
        user_posts_dict: Dict[int, List],
        limit: int = 10
    ) -> List:
        """
        Generate a basic feed for a user.
        
        Algorithm:
        1. Get posts from all followed users
        2. Rank by engagement score
        3. Return top posts
        
        Time Complexity: O(n log n) where n = total posts
        Space Complexity: O(n)
        
        Args:
            user_id: User requesting the feed
            following_list: Set of user IDs this user follows
            user_posts_dict: Dict mapping user_id → [posts]
            limit: Number of posts to return
            
        Returns:
            List of top ranked posts for the feed
        """
        # STEP 1: Collect posts from all followed users
        # Time: O(n) where n = total posts from following
        feed_posts = []
        
        for followed_user_id in following_list:
            if followed_user_id in user_posts_dict:
                # Extend feed with this user's posts
                feed_posts.extend(user_posts_dict[followed_user_id])
        
        # If no posts from following, return empty
        if not feed_posts:
            return []
        
        # STEP 2: Rank posts by engagement (O(n log n) Timsort)
        ranked_posts = FeedAlgorithm.rank_posts_by_engagement(feed_posts)
        
        # STEP 3: Return top limit posts (O(limit) ≈ O(1) for small limit)
        return ranked_posts[:limit]
    
    @staticmethod
    def generate_personalized_feed(
        user_id: int,
        following_list: set,
        user_posts_dict: Dict[int, List],
        current_user_likes: set,
        limit: int = 10
    ) -> List:
        """
        Generate a more personalized feed with filtering.
        
        Improvements:
        1. Don't show posts already liked
        2. Diversify (don't show same user's posts multiple times)
        3. Better user experience
        
        Args:
            user_id: User requesting feed
            following_list: Users being followed
            user_posts_dict: Posts by user
            current_user_likes: Posts user already liked
            limit: Number of posts to return
            
        Returns:
            List of personalized ranked posts
        """
        feed_posts = []
        user_post_counts = {}  # Track posts per user for diversity
        
        # STEP 1: Collect posts, excluding already liked
        for followed_user_id in following_list:
            if followed_user_id in user_posts_dict:
                for post in user_posts_dict[followed_user_id]:
                    # Skip posts user already liked
                    if post.post_id not in current_user_likes:
                        feed_posts.append(post)
                        user_post_counts[followed_user_id] = \
                            user_post_counts.get(followed_user_id, 0) + 1
        
        if not feed_posts:
            return []
        
        # STEP 2: Rank by engagement
        ranked_posts = FeedAlgorithm.rank_posts_by_engagement(feed_posts)
        
        # STEP 3: Diversify - limit posts per user
        diversified_posts = []
        user_post_limit_counts = {}
        max_posts_per_user = 2  # Max 2 posts from same person in feed
        
        for post in ranked_posts:
            user_id_author = post.user_id
            current_count = user_post_limit_counts.get(user_id_author, 0)
            
            # Only add if haven't reached max from this user
            if current_count < max_posts_per_user:
                diversified_posts.append(post)
                user_post_limit_counts[user_id_author] = current_count + 1
            
            # Stop if we have enough posts
            if len(diversified_posts) >= limit:
                break
        
        return diversified_posts