from social_media.services.graph_service import UserGraph

print("=== Test 1: Create Graph ===")
g = UserGraph()

# Create relationships
users = [1, 2, 3, 4, 5]

# User 1 follows: 2, 3, 4
g.add_edge(1, 2)
g.add_edge(1, 3)
g.add_edge(1, 4)

# User 5 follows: 2, 3, 5
g.add_edge(5, 2)
g.add_edge(5, 3)
g.add_edge(5, 5)

print("Graph created with relationships")

print("\n=== Test 2: Mutual Friends ===")
mutual = g.find_mutual_friends(1, 5)
print(f"User 1 follows: {g.get_following(1)}")
print(f"User 5 follows: {g.get_following(5)}")
print(f"Mutual friends: {mutual}")

# User 1 follows: {2, 3, 4}
# User 5 follows: {2, 3, 5}
# Mutual: {2, 3}
assert mutual == {2, 3}, "Mutual friends calculation wrong!"
print("✓ Mutual friends calculation correct!")

print("\n=== Test 3: Remove Edge ===")
result = g.remove_edge(1, 2)
print(f"Removed edge: {result}")
assert result == True
assert g.has_edge(1, 2) == False
print("✓ Edge removal works!")

print("\n✓ ALL TESTS PASSED!")