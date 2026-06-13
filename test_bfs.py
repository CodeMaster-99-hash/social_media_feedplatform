from social_media.services.graph_service import UserGraph

print("=== BFS Algorithm Test ===")
g = UserGraph()

# Create a chain of follows
# User 1 -> 2 -> 3 -> 4 -> 5
g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(4, 5)

print("\nGraph structure:")
print("1 follows 2")
print("2 follows 3")
print("3 follows 4")
print("4 follows 5")

print("\n=== Distance Tests ===")

# Distance 0: User 1 itself
distance_0 = g.find_users_at_distance(1, 0)
print(f"Distance 0 from user 1: {distance_0}")
assert distance_0 == [1], "Distance 0 should be [1]"
print("✓ Distance 0 correct")

# Distance 1: Users user 1 follows
distance_1 = g.find_users_at_distance(1, 1)
print(f"Distance 1 from user 1: {distance_1}")
assert distance_1 == [2], "Distance 1 should be [2]"
print("✓ Distance 1 correct")

# Distance 2: Users that distance-1 users follow
distance_2 = g.find_users_at_distance(1, 2)
print(f"Distance 2 from user 1: {distance_2}")
assert distance_2 == [3], "Distance 2 should be [3]"
print("✓ Distance 2 correct")

# Distance 3
distance_3 = g.find_users_at_distance(1, 3)
print(f"Distance 3 from user 1: {distance_3}")
assert distance_3 == [4], "Distance 3 should be [4]"
print("✓ Distance 3 correct")

# Distance 4
distance_4 = g.find_users_at_distance(1, 4)
print(f"Distance 4 from user 1: {distance_4}")
assert distance_4 == [5], "Distance 4 should be [5]"
print("✓ Distance 4 correct")

print("\n=== BFS TIME COMPLEXITY ===")
print("BFS Algorithm: O(V + E)")
print("V = number of vertices (users)")
print("E = number of edges (follows)")
print("For a chain of 5 users: O(5 + 4) = O(9)")
print("Efficient even for millions of users!")

print("\n✓ BFS ALGORITHM WORKS CORRECTLY!")