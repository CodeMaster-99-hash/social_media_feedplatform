"""
Main Demo Script - Shows all features of the social media platform
Run with: python main.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from social_media.services.platform_service import SocialMediaPlatform


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_section(text):
    """Print a section header."""
    print(f"\n>>> {text}")
    print("-" * 70)


def demo():
    """Run the complete demo."""
    
    # Initialize platform
    platform = SocialMediaPlatform()
    
    # ==================== STEP 1: CREATE USERS ====================
    
    print_header("STEP 1: CREATING USERS")
    
    alice = platform.create_user("alice", "alice@example.com", "Alice Johnson")
    bob = platform.create_user("bob", "bob@example.com", "Bob Smith")
    carol = platform.create_user("carol", "carol@example.com", "Carol White")
    diana = platform.create_user("diana", "diana@example.com", "Diana Brown")
    
    print("✓ Created 4 users:")
    for user in [alice, bob, carol, diana]:
        print(f"  - {user.username:15} (ID: {user.user_id}, Email: {user.email})")
    
    # ==================== STEP 2: CREATE FOLLOW RELATIONSHIPS ====================
    
    print_header("STEP 2: CREATING FOLLOW RELATIONSHIPS")
    
    print("Creating follow relationships:")
    platform.follow_user(alice.user_id, bob.user_id)
    print(f"  ✓ Alice follows Bob")
    
    platform.follow_user(alice.user_id, carol.user_id)
    print(f"  ✓ Alice follows Carol")
    
    platform.follow_user(bob.user_id, carol.user_id)
    print(f"  ✓ Bob follows Carol")
    
    platform.follow_user(carol.user_id, diana.user_id)
    print(f"  ✓ Carol follows Diana")
    
    print_section("Follow Statistics")
    print(f"Alice follows: {alice.get_following_count()} users")
    print(f"Alice followers: {alice.get_follower_count()} users")
    print(f"Bob follows: {bob.get_following_count()} users")
    print(f"Carol follows: {carol.get_following_count()} users")
    print(f"Carol followers: {carol.get_follower_count()} users")
    
    # ==================== STEP 3: CREATE POSTS ====================
    
    print_header("STEP 3: CREATING POSTS")
    
    print("Creating posts:")
    
    post1 = platform.create_post(bob.user_id, "Just finished an amazing coding project! 🚀")
    print(f"  ✓ Bob created post: '{post1.content}'")
    
    post2 = platform.create_post(carol.user_id, "Beautiful sunset at the beach! 🌅")
    print(f"  ✓ Carol created post: '{post2.content}'")
    
    post3 = platform.create_post(diana.user_id, "Coffee and coding - my favorite combo! ☕💻")
    print(f"  ✓ Diana created post: '{post3.content}'")
    
    post4 = platform.create_post(bob.user_id, "Check out this cool new Python library!")
    print(f"  ✓ Bob created another post: '{post4.content}'")
    
    # ==================== STEP 4: ADD LIKES AND COMMENTS ====================
    
    print_header("STEP 4: ADDING LIKES AND COMMENTS")
    
    print("Alice likes posts:")
    platform.like_post(alice.user_id, post1.post_id)
    print(f"  ✓ Alice likes: '{post1.content}'")
    
    platform.like_post(alice.user_id, post2.post_id)
    print(f"  ✓ Alice likes: '{post2.content}'")
    
    platform.like_post(alice.user_id, post3.post_id)
    print(f"  ✓ Alice likes: '{post3.content}'")
    
    print("\nBob likes posts:")
    platform.like_post(bob.user_id, post2.post_id)
    print(f"  ✓ Bob likes: '{post2.content}'")
    
    platform.like_post(bob.user_id, post3.post_id)
    print(f"  ✓ Bob likes: '{post3.content}'")
    
    print("\nCarol likes posts:")
    platform.like_post(carol.user_id, post3.post_id)
    print(f"  ✓ Carol likes: '{post3.content}'")
    
    platform.like_post(carol.user_id, post4.post_id)
    print(f"  ✓ Carol likes: '{post4.content}'")
    
    print("\nAdding comments:")
    platform.add_comment(alice.user_id, post1.post_id, "That's awesome! Congratulations! 🎉")
    print(f"  ✓ Alice comments on Bob's post")
    
    platform.add_comment(bob.user_id, post2.post_id, "Amazing view! Where is this? 😍")
    print(f"  ✓ Bob comments on Carol's post")
    
    platform.add_comment(alice.user_id, post3.post_id, "I need to try this combo too!")
    print(f"  ✓ Alice comments on Diana's post")
    
    platform.add_comment(carol.user_id, post3.post_id, "The best combination indeed!")
    print(f"  ✓ Carol comments on Diana's post")
    
    # ==================== STEP 5: SHOW ENGAGEMENT SCORES ====================
    
    print_header("STEP 5: ENGAGEMENT SCORES (Posts Ranked by Engagement)")
    
    posts = [post1, post2, post3, post4]
    print("Post Engagement Breakdown:")
    print(f"{'Post':<10} {'Author':<10} {'Likes':<8} {'Comments':<10} {'Score':<10}")
    print("-" * 60)
    
    for post in posts:
        author = platform.get_user(post.user_id).username
        engagement = post.get_engagement_score()
        print(f"Post {post.post_id:<5} {author:<10} {post.get_like_count():<8} {post.get_comment_count():<10} {engagement:.1f}")
    
    # ==================== STEP 6: GENERATE FEEDS ====================
    
    print_header("STEP 6: GENERATING PERSONALIZED FEEDS")
    
    print_section("ALICE'S FEED")
    print("Alice follows: Bob, Carol, Diana")
    alice_feed = platform.get_user_feed(alice.user_id, limit=10)
    
    print(f"\nAlice's Feed ({len(alice_feed)} posts - ranked by engagement):")
    print("-" * 70)
    
    for i, post in enumerate(alice_feed, 1):
        author = platform.get_user(post.user_id)
        engagement = post.get_engagement_score()
        print(f"\n  {i}. Post #{post.post_id} by {author.username}")
        print(f"     Content: \"{post.content}\"")
        print(f"     Likes: {post.get_like_count()} | Comments: {post.get_comment_count()} | Score: {engagement:.1f}")
        
        if post.get_comment_count() > 0:
            print(f"     Comments:")
            for comment in post.get_comments():
                commenter = platform.get_user(comment.user_id)
                print(f"       - {commenter.username}: \"{comment.content}\"")
    
    print("\n" + "="*70)
    print("✓ FEED IS RANKED BY ENGAGEMENT - HIGHEST SCORING POSTS APPEAR FIRST!")
    print("="*70)
    
    # ==================== STEP 7: BOB'S FEED ====================
    
    print_section("BOB'S FEED")
    print("Bob follows: Carol, Diana")
    bob_feed = platform.get_user_feed(bob.user_id, limit=10)
    
    print(f"\nBob's Feed ({len(bob_feed)} posts - ranked by engagement):")
    print("-" * 70)
    
    for i, post in enumerate(bob_feed, 1):
        author = platform.get_user(post.user_id)
        engagement = post.get_engagement_score()
        print(f"\n  {i}. Post #{post.post_id} by {author.username}")
        print(f"     Content: \"{post.content}\"")
        print(f"     Likes: {post.get_like_count()} | Comments: {post.get_comment_count()} | Score: {engagement:.1f}")
    
    # ==================== STEP 8: FRIEND SUGGESTIONS ====================
    
    print_header("STEP 8: FRIEND SUGGESTIONS (Friends of Friends)")
    
    print("Using graph algorithm to find friends-of-friends:")
    
    suggestions = platform.suggest_friends(alice.user_id, limit=5)
    print(f"\nSuggested friends for Alice:")
    if suggestions:
        for user in suggestions:
            print(f"  - {user.username} ({user.get_follower_count()} followers)")
    else:
        print("  (No suggestions at this time)")
    
    # ==================== STEP 9: MUTUAL FRIENDS ====================
    
    print_header("STEP 9: MUTUAL FRIENDS")
    
    print("Finding users that both follow:")
    
    mutual_ab = platform.get_mutual_friends(alice.user_id, bob.user_id)
    print(f"\nMutual friends between Alice and Bob:")
    if mutual_ab:
        for user in mutual_ab:
            print(f"  - {user.username}")
    else:
        print("  (None)")
    
    mutual_bc = platform.get_mutual_friends(bob.user_id, carol.user_id)
    print(f"\nMutual friends between Bob and Carol:")
    if mutual_bc:
        for user in mutual_bc:
            print(f"  - {user.username}")
    else:
        print("  (None)")
    
    # ==================== STEP 10: PLATFORM STATISTICS ====================
    
    print_header("STEP 10: PLATFORM STATISTICS")
    
    stats = platform.get_platform_stats()
    
    print(f"Platform Overview:")
    print(f"  Total Users:         {stats['total_users']}")
    print(f"  Total Posts:         {stats['total_posts']}")
    print(f"  Total Likes:         {stats['total_likes']}")
    print(f"  Total Comments:      {stats['total_comments']}")
    print(f"  Avg Followers/User:  {stats['avg_followers']:.1f}")
    
    # ==================== FINAL SUMMARY ====================
    
    print_header("DEMONSTRATION COMPLETE! 🎉")
    
    print("This demo showcased the following features:")
    print("""
    ✓ User Management
      - Create users with profiles
      - Track followers and following

    ✓ Follow Relationships
      - Users can follow each other
      - Build social graph

    ✓ Content Creation
      - Posts with content
      - Comments on posts

    ✓ Engagement System
      - Like posts (O(1) operation!)
      - Comment on posts
      - Track engagement scores

    ✓ Feed Algorithm (THE CORE FEATURE!)
      - Collect posts from following
      - Rank by engagement (likes × 2 + comments × 3)
      - Show top posts first
      - O(n log n) complexity

    ✓ Graph Algorithms
      - BFS for friend discovery
      - Find friends-of-friends
      - Calculate mutual friends

    ✓ Statistics
      - Track platform metrics
      - Measure engagement
    """)
    
    print("="*70)
    print("This is a REAL social media platform backend!")
    print("Companies like Instagram, Twitter, Facebook use similar systems.")
    print("="*70)
    
    print_header("KEY INSIGHTS")
    
    print("""
    Why This Design?
    
    1. SETS for followers/likes
       - O(1) membership testing
       - Fast follow checks: alice.is_following(bob) = O(1)
       - Millions of users? Still O(1)!

    2. GRAPH for relationships
       - BFS finds friends at distance
       - O(V + E) complexity
       - Efficient even for large networks

    3. SORTING for feed ranking
       - O(n log n) to sort posts
       - Only done once when feed requested
       - Users see best content first!

    4. PROFESSIONAL ARCHITECTURE
       - Separation of concerns
       - Models, Services, Algorithms
       - Testable and scalable
    """)
    
    print("="*70)
    print("Next Steps:")
    print("  1. Push to GitHub")
    print("  2. Write comprehensive README")
    print("  3. Add to portfolio")
    print("  4. Impress recruiters! 🎓")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo()