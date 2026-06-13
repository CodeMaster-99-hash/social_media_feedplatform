"""
Unit tests for the social media platform
Using pytest framework
"""
import pytest
from social_media.services.platform_service import SocialMediaPlatform


class TestPlatform:
    """Test suite for SocialMediaPlatform"""
    
    @pytest.fixture
    def platform(self):
        """Create a fresh platform for each test."""
        return SocialMediaPlatform()
    
    # ==================== USER TESTS ====================
    
    def test_create_user(self, platform):
        """Test creating a new user."""
        user = platform.create_user("alice", "alice@example.com", "Alice")
        
        assert user.user_id == 1
        assert user.username == "alice"
        assert user.get_follower_count() == 0
        assert user.get_following_count() == 0
    
    def test_create_duplicate_username(self, platform):
        """Test that duplicate usernames are rejected."""
        platform.create_user("alice", "alice@example.com")
        
        with pytest.raises(ValueError):
            platform.create_user("alice", "alice2@example.com")
    
    def test_get_user(self, platform):
        """Test getting a user by ID."""
        user = platform.create_user("alice", "alice@example.com")
        retrieved = platform.get_user(user.user_id)
        
        assert retrieved is not None
        assert retrieved.username == "alice"
    
    def test_get_user_by_username(self, platform):
        """Test getting a user by username."""
        user = platform.create_user("alice", "alice@example.com")
        retrieved = platform.get_user_by_username("alice")
        
        assert retrieved is not None
        assert retrieved.user_id == user.user_id
    
    # ==================== FOLLOW TESTS ====================
    
    def test_follow_user(self, platform):
        """Test one user following another."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        
        success = platform.follow_user(alice.user_id, bob.user_id)
        
        assert success
        assert bob.user_id in alice.following
        assert alice.user_id in bob.followers
    
    def test_follow_nonexistent_user(self, platform):
        """Test that following nonexistent user raises error."""
        alice = platform.create_user("alice", "alice@example.com")
        
        with pytest.raises(ValueError):
            platform.follow_user(alice.user_id, 999)
    
    def test_unfollow_user(self, platform):
        """Test unfollowing a user."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        
        platform.follow_user(alice.user_id, bob.user_id)
        success = platform.unfollow_user(alice.user_id, bob.user_id)
        
        assert success
        assert bob.user_id not in alice.following
    
    # ==================== POST TESTS ====================
    
    def test_create_post(self, platform):
        """Test creating a post."""
        alice = platform.create_user("alice", "alice@example.com")
        post = platform.create_post(alice.user_id, "Hello World!")
        
        assert post.post_id == 1
        assert post.user_id == alice.user_id
        assert post.content == "Hello World!"
        assert post.get_engagement_score() == 0
    
    def test_create_empty_post(self, platform):
        """Test that empty posts are rejected."""
        alice = platform.create_user("alice", "alice@example.com")
        
        with pytest.raises(ValueError):
            platform.create_post(alice.user_id, "")
    
    def test_like_post(self, platform):
        """Test liking a post."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        
        post = platform.create_post(alice.user_id, "Hello!")
        success = platform.like_post(bob.user_id, post.post_id)
        
        assert success
        assert post.get_like_count() == 1
        assert bob.user_id in post.likes
    
    def test_unlike_post(self, platform):
        """Test unliking a post."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        
        post = platform.create_post(alice.user_id, "Hello!")
        platform.like_post(bob.user_id, post.post_id)
        success = platform.unlike_post(bob.user_id, post.post_id)
        
        assert success
        assert post.get_like_count() == 0
    
    def test_like_same_post_twice(self, platform):
        """Test that liking same post twice fails."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        
        post = platform.create_post(alice.user_id, "Hello!")
        success1 = platform.like_post(bob.user_id, post.post_id)
        success2 = platform.like_post(bob.user_id, post.post_id)
        
        assert success1 == True
        assert success2 == False
        assert post.get_like_count() == 1
    
    # ==================== COMMENT TESTS ====================
    
    def test_add_comment(self, platform):
        """Test adding a comment to a post."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        
        post = platform.create_post(alice.user_id, "Hello!")
        comment = platform.add_comment(bob.user_id, post.post_id, "Nice!")
        
        assert comment.comment_id == 1
        assert post.get_comment_count() == 1
    
    def test_add_empty_comment(self, platform):
        """Test that empty comments are rejected."""
        alice = platform.create_user("alice", "alice@example.com")
        post = platform.create_post(alice.user_id, "Hello!")
        
        with pytest.raises(ValueError):
            platform.add_comment(alice.user_id, post.post_id, "")
    
    # ==================== FEED TESTS ====================
    
    def test_get_feed_basic(self, platform):
        """Test generating a basic feed."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        
        platform.follow_user(alice.user_id, bob.user_id)
        post = platform.create_post(bob.user_id, "Bob's post")
        
        feed = platform.get_user_feed(alice.user_id)
        
        assert len(feed) == 1
        assert feed[0].post_id == post.post_id
    
    def test_feed_ranking(self, platform):
        """Test that posts are ranked by engagement."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        carol = platform.create_user("carol", "carol@example.com")
        
        platform.follow_user(alice.user_id, bob.user_id)
        platform.follow_user(alice.user_id, carol.user_id)
        
        post1 = platform.create_post(bob.user_id, "Post 1")
        post2 = platform.create_post(carol.user_id, "Post 2")
        
        # Like post2 more
        for i in range(5):
            user = platform.create_user(f"user{i}", f"user{i}@example.com")
            platform.like_post(user.user_id, post2.post_id)
        
        feed = platform.get_user_feed(alice.user_id)
        
        # post2 should be first (more likes)
        assert feed[0].post_id == post2.post_id
        assert feed[1].post_id == post1.post_id
    
    def test_empty_feed(self, platform):
        """Test feed is empty if not following anyone."""
        alice = platform.create_user("alice", "alice@example.com")
        feed = platform.get_user_feed(alice.user_id)
        
        assert feed == []
    
    def test_personalized_feed(self, platform):
        """Test personalized feed excludes liked posts."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        
        platform.follow_user(alice.user_id, bob.user_id)
        
        post1 = platform.create_post(bob.user_id, "Post 1")
        post2 = platform.create_post(bob.user_id, "Post 2")
        
        # Alice likes post1
        platform.like_post(alice.user_id, post1.post_id)
        
        # Get personalized feed
        feed = platform.get_personalized_feed(alice.user_id)
        
        # post1 should be excluded
        assert post1.post_id not in [p.post_id for p in feed]
        assert post2.post_id in [p.post_id for p in feed]
    
    # ==================== GRAPH TESTS ====================
    
    def test_suggest_friends(self, platform):
        """Test friend suggestions."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        carol = platform.create_user("carol", "carol@example.com")
        diana = platform.create_user("diana", "diana@example.com")
        
        platform.follow_user(alice.user_id, bob.user_id)
        platform.follow_user(bob.user_id, carol.user_id)
        platform.follow_user(bob.user_id, diana.user_id)
        
        suggestions = platform.suggest_friends(alice.user_id)
        suggested_ids = [u.user_id for u in suggestions]
        
        # Carol and Diana should be suggested (friends of Bob)
        assert carol.user_id in suggested_ids or diana.user_id in suggested_ids
    
    def test_mutual_friends(self, platform):
        """Test mutual friends calculation."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        carol = platform.create_user("carol", "carol@example.com")
        
        platform.follow_user(alice.user_id, carol.user_id)
        platform.follow_user(bob.user_id, carol.user_id)
        
        mutual = platform.get_mutual_friends(alice.user_id, bob.user_id)
        mutual_ids = [u.user_id for u in mutual]
        
        assert carol.user_id in mutual_ids
    
    # ==================== STATISTICS TESTS ====================
    
    def test_platform_stats(self, platform):
        """Test platform statistics."""
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        
        post = platform.create_post(alice.user_id, "Hello!")
        platform.like_post(bob.user_id, post.post_id)
        platform.add_comment(bob.user_id, post.post_id, "Nice!")
        
        stats = platform.get_platform_stats()
        
        assert stats['total_users'] == 2
        assert stats['total_posts'] == 1
        assert stats['total_likes'] == 1
        assert stats['total_comments'] == 1
    
    # ==================== INTEGRATION TESTS ====================
    
    def test_complete_workflow(self, platform):
        """Test complete workflow: users, follows, posts, feed."""
        # Create users
        alice = platform.create_user("alice", "alice@example.com")
        bob = platform.create_user("bob", "bob@example.com")
        carol = platform.create_user("carol", "carol@example.com")
        
        # Create relationships
        platform.follow_user(alice.user_id, bob.user_id)
        platform.follow_user(alice.user_id, carol.user_id)
        
        # Create posts
        post1 = platform.create_post(bob.user_id, "Bob's post")
        post2 = platform.create_post(carol.user_id, "Carol's post")
        
        # Add engagement
        platform.like_post(alice.user_id, post1.post_id)
        platform.like_post(alice.user_id, post2.post_id)
        platform.like_post(alice.user_id, post2.post_id)  # Try to like again
        
        platform.add_comment(alice.user_id, post1.post_id, "Great!")
        platform.add_comment(alice.user_id, post2.post_id, "Amazing!")
        platform.add_comment(bob.user_id, post2.post_id, "Thanks!")
        
        # Get feed
        feed = platform.get_user_feed(alice.user_id)
        
        # post2 has more engagement
        assert len(feed) == 2
        assert feed[0].post_id == post2.post_id