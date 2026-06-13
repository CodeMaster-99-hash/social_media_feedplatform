from social_media.models.post import Post
from social_media.algorithms.feed_algorithm import FeedAlgorithm

print("=== Feed Algorithm Test ===")

# Create posts
post1 = Post(1, 1, "Post 1")  # 0 engagement
post2 = Post(2, 1, "Post 2")  # 10 engagement
post3 = Post(3, 1, "Post 3")  # 6 engagement

print("\n=== Test 1: Add Engagement ===")

# Post 2: 5 likes = 10 points
post2.add_like(1)
post2.add_like(2)
post2.add_like(3)
post2.add_like(4)
post2.add_like(5)

# Post 3: 3 likes = 6 points
post3.add_like(1)
post3.add_like(2)
post3.add_like(3)

print(f"Post 1 engagement: {post1.get_engagement_score()}")
print(f"Post 2 engagement: {post2.get_engagement_score()}")
print(f"Post 3 engagement: {post3.get_engagement_score()}")

print("\n=== Test 2: Rank Posts ===")

posts = [post1, post2, post3]
ranked = FeedAlgorithm.rank_posts_by_engagement(posts)

print("Before ranking:", [p.post_id for p in posts])
print("After ranking:", [p.post_id for p in ranked])

# Should be: post2 (10), post3 (6), post1 (0)
assert ranked[0].post_id == 2, "Post 2 should be first"
assert ranked[1].post_id == 3, "Post 3 should be second"
assert ranked[2].post_id == 1, "Post 1 should be third"

print("✓ Posts correctly ranked by engagement!")

print("\n=== Test 3: Generate Feed ===")

# Create user posts dict
user_posts_dict = {
    1: [post1, post2],
    2: [post3]
}

following_list = {1, 2}

feed = FeedAlgorithm.generate_feed(
    user_id=100,
    following_list=following_list,
    user_posts_dict=user_posts_dict,
    limit=10
)

print(f"Generated feed (top 3): {[p.post_id for p in feed]}")

# Should be ranked: post2, post3, post1
assert feed[0].post_id == 2, "Post 2 should be first"
assert feed[1].post_id == 3, "Post 3 should be second"
assert feed[2].post_id == 1, "Post 1 should be third"

print("✓ Feed generated correctly!")

print("\n=== Test 4: Personalized Feed ===")

# User already liked post 2
liked_posts = {2}

personalized = FeedAlgorithm.generate_personalized_feed(
    user_id=100,
    following_list=following_list,
    user_posts_dict=user_posts_dict,
    current_user_likes=liked_posts,
    limit=10
)

print(f"Personalized feed (excluding liked): {[p.post_id for p in personalized]}")

# Should not include post 2
assert 2 not in [p.post_id for p in personalized], "Post 2 should be excluded"

print("✓ Personalized feed works!")

print("\n✓ ALL FEED ALGORITHM TESTS PASSED!")