"""
Graph Service - Manages user relationships as a graph
Implements graph algorithms like BFS
"""
from typing import Set, List
from collections import deque, defaultdict


class UserGraph:
    """
    Graph representation of user relationships.
    
    Uses adjacency list for efficient lookups.
    
    Key points:
    - Each user is a node
    - Follow relationship is a directed edge
    - adjacency_list[user_a] = set of users that user_a follows
    """
    
    def __init__(self):
        """Initialize empty graph."""
        # adjacency_list[user_id] = Set of user IDs this user follows
        # Using defaultdict(set) for automatic set creation
        self.adjacency_list: dict = defaultdict(set)
    
    def add_edge(self, from_user: int, to_user: int) -> None:
        """
        Add an edge (user A follows user B).
        Time: O(1) operation!
        
        Args:
            from_user: User who is following
            to_user: User being followed
        """
        # Add edge to adjacency list
        # Set.add() is O(1) operation
        self.adjacency_list[from_user].add(to_user)
    
    def remove_edge(self, from_user: int, to_user: int) -> bool:
        """
        Remove an edge (user A unfollows user B).
        Time: O(1) operation!
        
        Args:
            from_user: User unfollowing
            to_user: User being unfollowed
            
        Returns:
            True if removed, False if didn't exist
        """
        # Check if edge exists
        if to_user in self.adjacency_list[from_user]:
            # Remove edge
            self.adjacency_list[from_user].discard(to_user)
            return True
        return False
    
    def has_edge(self, from_user: int, to_user: int) -> bool:
        """
        Check if user A follows user B.
        Time: O(1) operation!
        
        Args:
            from_user: Follower
            to_user: Followed user
            
        Returns:
            True if follows, False otherwise
        """
        return to_user in self.adjacency_list[from_user]
    
    def get_following(self, user_id: int) -> Set[int]:
        """
        Get all users that a user follows.
        Time: O(1) to return the set!
        
        Args:
            user_id: User ID
            
        Returns:
            Set of user IDs being followed
        """
        return self.adjacency_list[user_id].copy()
    
    def get_followers(self, user_id: int) -> Set[int]:
        """
        Get all users who follow a user.
        Time: O(n) operation (must check all users).
        
        Args:
            user_id: User ID
            
        Returns:
            Set of followers
        """
        followers = set()
        # Check every user to see if they follow this user
        for follower_id, following_set in self.adjacency_list.items():
            if user_id in following_set:
                followers.add(follower_id)
        return followers
    
    def find_mutual_friends(self, user_a: int, user_b: int) -> Set[int]:
        """
        Find mutual friends between two users.
        
        Mutual friends = people that both users follow
        Time: O(min(a, b)) using set intersection!
        
        Example:
        User A follows: {1, 2, 3, 4}
        User B follows: {2, 3, 5, 6}
        Mutual: {2, 3}
        
        Args:
            user_a: First user
            user_b: Second user
            
        Returns:
            Set of mutual friend IDs
        """
        # Get who each user follows
        following_a = self.adjacency_list[user_a]
        following_b = self.adjacency_list[user_b]
        
        # Set intersection is efficient!
        # & operator does set intersection
        return following_a & following_b
    
    def find_users_at_distance(self, start_user: int, distance: int) -> List[int]:
        """
        Find all users at a specific distance using BFS.
        
        Distance 1: Users this person follows
        Distance 2: Users that those users follow
        Distance 3: And so on...
        
        Time: O(V + E) where V=vertices (users), E=edges (follows)
        
        BFS Algorithm:
        1. Start with start_user at distance 0
        2. Use queue to process level by level
        3. Each iteration goes one distance further
        4. Track visited nodes to avoid cycles
        5. Return all nodes at target distance
        
        Args:
            start_user: Starting user
            distance: Distance to find
            
        Returns:
            List of user IDs at that distance
        """
        # Validate input
        if distance < 0:
            raise ValueError("Distance must be non-negative!")
        
        # Track visited nodes to avoid cycles/duplicates
        visited = set()
        
        # Queue stores (user_id, current_distance)
        # deque is O(1) for append and popleft
        queue = deque([(start_user, 0)])
        
        # List to store users at target distance
        users_at_distance = []
        
        # BFS Main Loop
        while queue:
            # Get next user from front of queue
            current_user, current_distance = queue.popleft()
            
            # Skip if already visited
            if current_user in visited:
                continue
            
            # Mark as visited
            visited.add(current_user)
            
            # If we've reached target distance, add to results
            if current_distance == distance:
                users_at_distance.append(current_user)
            
            # If we haven't reached target distance yet, explore further
            elif current_distance < distance:
                # Add all following users to queue
                for following_user in self.adjacency_list[current_user]:
                    if following_user not in visited:
                        # Add to queue with incremented distance
                        queue.append((following_user, current_distance + 1))
        
        return users_at_distance
    
    def find_path(self, from_user: int, to_user: int) -> List[int]:
        """
        Find shortest path between two users using BFS.
        
        Example:
        Path from A to D: A -> B -> C -> D
        Returns: [A, B, C, D]
        
        Time: O(V + E)
        
        Args:
            from_user: Start user
            to_user: Target user
            
        Returns:
            List of user IDs representing path, empty if no path
        """
        # If same user, return self
        if from_user == to_user:
            return [from_user]
        
        # Track visited nodes
        visited = set()
        
        # Queue stores (user_id, path_so_far)
        queue = deque([(from_user, [from_user])])
        
        # BFS Main Loop
        while queue:
            current_user, path = queue.popleft()
            
            # Skip if already visited
            if current_user in visited:
                continue
            
            # Mark as visited
            visited.add(current_user)
            
            # Check each user this person follows
            for following_user in self.adjacency_list[current_user]:
                # If found target, return path
                if following_user == to_user:
                    return path + [to_user]
                
                # Otherwise, add to queue for exploration
                if following_user not in visited:
                    queue.append((following_user, path + [following_user]))
        
        # No path found
        return []
    
    def suggest_friends(self, user_id: int, limit: int = 5) -> List[int]:
        """
        Suggest users to follow (friends of friends).
        
        Algorithm:
        1. Get all users this person follows (distance 1)
        2. Get all users those people follow (distance 2)
        3. Exclude users already following
        4. Return top suggestions
        
        Time: O(V + E)
        
        Example:
        User A follows: {B, C}
        B follows: {D, E}
        C follows: {E, F}
        Suggestions for A: {D, E, F} (excluding A, B, C)
        
        Args:
            user_id: User to get suggestions for
            limit: How many suggestions to return
            
        Returns:
            List of suggested user IDs
        """
        # Get users already following
        already_following = self.adjacency_list[user_id]
        
        # Get distance-2 users (friends of friends)
        suggestions = set()
        
        # For each user this person follows
        for direct_follow in already_following:
            # Add all users they follow
            suggestions.update(self.adjacency_list[direct_follow])
        
        # Remove self and already following
        suggestions.discard(user_id)
        suggestions -= already_following
        
        # Return limit number of suggestions
        return list(suggestions)[:limit]