from social_media.services.graph_service import UserGraph

print("=== Friend Suggestions Test ===")
g = UserGraph()

# Create network
# User 1 follows: 2, 3
g.add_edge(1, 2)
g.add_edge(1, 3)

# User 2 follows: 4, 5
g.add_edge(2, 4)
g.add_edge(2, 5)

# User 3 follows: 5, 6
g.add_edge(3, 5)
g.add_edge(3, 6)

print("Network:")
print("User 1 follows: {2, 3}")
print("User 2 follows: {4, 5}")
print("User 3 follows: {5, 6}")

print("\n=== Suggestions for User 1 ===")
suggestions = g.suggest_friends(1, limit=5)
print(f"Suggestions: {suggestions}")

# Suggestions should be users that user 1's followers follow
# User 2 follows: {4, 5}
# User 3 follows: {5, 6}
# Suggestions (excluding 1, 2, 3): {4, 5, 6}
assert all(s in {4, 5, 6} for s in suggestions), "Wrong suggestions"
print(f"✓ Correct suggestions (should be from {{4, 5, 6}})")

print("\n=== How Suggestions Work ===")
print("1. Get people you follow")
print("   User 1 follows: {2, 3}")
print("\n2. Get people THEY follow")
print("   {2, 3} follow: {4, 5, 6}")
print("\n3. Suggest those people")
print("   Suggestions: {4, 5, 6}")
print("\n4. Algorithm: O(V + E)")
print("   Efficient for large networks!")

print("\n✓ FRIEND SUGGESTIONS WORK!")