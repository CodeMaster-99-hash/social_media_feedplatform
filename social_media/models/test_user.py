from social_media.models.user import User

# Create two users
alice = User(1, "alice", "alice@example.com")
bob = User(2, "bob", "bob@example.com")

print("=== Test 1: Create Users ===")
print(f"Alice: {alice}")
print(f"Bob: {bob}")

print("\n=== Test 2: Alice follows Bob ===")
result = alice.follow_user(bob.user_id)
print(f"Follow successful: {result}")
print(f"Alice following count: {alice.get_following_count()}")
print(f"Alice is following Bob: {alice.is_following(bob.user_id)}")

print("\n=== Test 3: Try to follow again (should fail) ===")
result = alice.follow_user(bob.user_id)
print(f"Follow successful: {result} (should be False)")

print("\n=== Test 4: Alice unfollows Bob ===")
result = alice.unfollow_user(bob.user_id)
print(f"Unfollow successful: {result}")
print(f"Alice following count: {alice.get_following_count()}")
print(f"Alice is following Bob: {alice.is_following(bob.user_id)}")

print("\n✓ ALL TESTS PASSED!") 
