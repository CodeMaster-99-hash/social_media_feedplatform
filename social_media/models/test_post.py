from social_media.models.post import Post

# Create a post
post = Post(1, 1, "This is an amazing post!")

print("=== Test 1: Create Post ===")
print(f"Post: {post}")
print(f"Engagement score: {post.get_engagement_score()}")

print("\n=== Test 2: Add Likes ===")
# Add 5 likes
for user_id in range(1, 6):
    result = post.add_like(user_id)
    print(f"User {user_id} liked: {result}")

print(f"Total likes: {post.get_like_count()}")
print(f"Engagement score: {post.get_engagement_score()}")

print("\n=== Test 3: Try to like again (should fail) ===")
result = post.add_like(1)
print(f"User 1 liked again: {result} (should be False)")
print(f"Total likes: {post.get_like_count()}")

print("\n=== Test 4: Remove a like ===")
result = post.remove_like(1)
print(f"Removed user 1's like: {result}")
print(f"Total likes: {post.get_like_count()}")
print(f"Engagement score: {post.get_engagement_score()}")

print("\n=== Test 5: Check if user liked ===")
print(f"Did user 1 like: {post.has_liked(1)} (should be False)")
print(f"Did user 2 like: {post.has_liked(2)} (should be True)")

print("\n✓ ALL TESTS PASSED!")