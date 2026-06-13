from social_media.services.platform_service import SocialMediaPlatform

print("=== THE MAIN FEATURE: get_user_feed() ===\n")

# Create platform
platform = SocialMediaPlatform()

# Create users
alice = platform.create_user("alice", "alice@example.com", "Alice")
bob = platform.create_user("bob", "bob@example.com", "Bob")
carol = platform.create_user("carol", "carol@example.com", "Carol")
diana = platform.create_user("diana", "diana@example.com", "Diana")

print("1. Created 4 users: Alice, Bob, Carol, Diana")

# Create relationships
platform.follow_user(alice.user_id, bob.user_id)
platform.follow_user(alice.user_id, carol.user_id)
platform.follow_user(alice.user_id, diana.user_id)

print("2. Alice follows: Bob, Carol, Diana")

# Create posts
post1 = platform.create_post(bob.user_id, "Bob's amazing post!")
post2 = platform.create_post(carol.user_id, "Carol's wonderful post!")
post3 = platform.create_post(diana.user_id, "Diana's great post!")

print("3. Created 3 posts (Bob, Carol, Diana)")

# Add engagement
platform.like_post(alice.user_id, post1.post_id)
platform.like_post(alice.user_id, post1.post_id)  # Try to like again
platform.like_post(carol.user_id, post1.post_id)

# Post1: 2 likes = 4 points
for i in range(5):
    platform.like_post(alice.user_id if i < 2 else carol.user_id, post2.post_id)

# Post2: 5 likes = 10 points (HIGHEST!)
for i in range(3):
    platform.like_post(alice.user_id, post3.post_id)

# Post3: 3 likes = 6 points

print("4. Added likes (engagement):")
print(f"   Post 1 (Bob): {post1.get_like_count()} likes = {post1.get_engagement_score()} points")
print(f"   Post 2 (Carol): {post2.get_like_count()} likes = {post2.get_engagement_score()} points")
print(f"   Post 3 (Diana): {post3.get_like_count()} likes = {post3.get_engagement_score()} points")

print("\n5. Generating Alice's Feed:")
feed = platform.get_user_feed(alice.user_id, limit=10)

print(f"   Feed size: {len(feed)} posts")
for i, post in enumerate(feed, 1):
    author = platform.get_user(post.user_id)
    print(f"   {i}. {author.username}'s post (score: {post.get_engagement_score()})")

# Feed should be ranked by engagement: Post2, Post3, Post1
assert feed[0].post_id == post2.post_id, "Post2 should be first (highest engagement)"
assert feed[1].post_id == post3.post_id, "Post3 should be second"
assert feed[2].post_id == post1.post_id, "Post1 should be third"

print("\n✓ FEED CORRECTLY RANKED BY ENGAGEMENT!")
print("\nThis is the core feature of social media:")
print("Users see the MOST ENGAGING posts FIRST!")
print("\n✓ ALL PLATFORM TESTS PASSED!")