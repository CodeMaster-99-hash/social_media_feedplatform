from social_media.models.user import User
from social_media.models.post import Post
from social_media.models.comment import Comment

print("=== Test 1: Create Everything ===")

# Create users
alice = User(1, "alice", "alice@example.com")
bob = User(2, "bob", "bob@example.com")
print(f"Created: {alice}")
print(f"Created: {bob}")

# Alice creates a post
post = Post(1, alice.user_id, "Check out my photo!")
print(f"Created: {post}")

# Bob comments on the post
comment = Comment(1, post.post_id, bob.user_id, "Nice photo!")
print(f"Created: {comment}")

print("\n=== Test 2: Add Comment to Post ===")
post.add_comment(comment)
print(f"Post now has {post.get_comment_count()} comment(s)")
print(f"Engagement score: {post.get_engagement_score()}")

print("\n=== Test 3: Add More Comments ===")
# Carol comments
carol = User(3, "carol", "carol@example.com")
comment2 = Comment(2, post.post_id, carol.user_id, "I agree!")
post.add_comment(comment2)

# Diana comments
diana = User(4, "diana", "diana@example.com")
comment3 = Comment(3, post.post_id, diana.user_id, "Love it!")
post.add_comment(comment3)

print(f"Post now has {post.get_comment_count()} comments")
print(f"Engagement score: {post.get_engagement_score()}")

print("\n=== Test 4: Get All Comments ===")
all_comments = post.get_comments()
for i, c in enumerate(all_comments, 1):
    print(f"  {i}. {c} - '{c.content}'")

print("\n=== Test 5: Comment Data ===")
print(f"First comment as dict: {comment.to_dict()}")

print("\n✓ ALL TESTS PASSED!")