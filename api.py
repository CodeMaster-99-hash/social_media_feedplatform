"""
FastAPI REST API for Social Media Platform
Deploy to Render with this file!
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from social_media.services.platform_service import SocialMediaPlatform

# Initialize FastAPI app
app = FastAPI(
    title="Social Media Platform API",
    description="Social media platform with feed algorithm and graph algorithms",
    version="1.0.0"
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global platform instance
platform = SocialMediaPlatform()

# ==================== PYDANTIC MODELS ====================

class UserCreate(BaseModel):
    """Model for creating a user"""
    username: str
    email: str
    name: Optional[str] = None

class UserResponse(BaseModel):
    """Model for user response"""
    user_id: int
    username: str
    email: str
    follower_count: int
    following_count: int

class PostCreate(BaseModel):
    """Model for creating a post"""
    user_id: int
    content: str

class PostResponse(BaseModel):
    """Model for post response"""
    post_id: int
    user_id: int
    content: str
    like_count: int
    comment_count: int
    engagement_score: float

class CommentCreate(BaseModel):
    """Model for creating a comment"""
    user_id: int
    post_id: int
    content: str

# ==================== ROOT ENDPOINT ====================

@app.get("/")
def read_root():
    """Root endpoint - API is alive!"""
    return {
        "message": "Social Media Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "github": "https://github.com/CodeMaster-99-hash/social-media-platform"
    }

@app.get("/health")
def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy", "service": "social-media-platform"}

# ==================== USER ENDPOINTS ====================

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    """Create a new user"""
    try:
        new_user = platform.create_user(
            user.username,
            user.email,
            user.name or ""
        )
        return {
            "user_id": new_user.user_id,
            "username": new_user.username,
            "email": new_user.email,
            "follower_count": new_user.get_follower_count(),
            "following_count": new_user.get_following_count()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Get user by ID"""
    user = platform.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "follower_count": user.get_follower_count(),
        "following_count": user.get_following_count()
    }

@app.post("/users/{user_id}/follow/{follow_id}")
def follow_user(user_id: int, follow_id: int):
    """Follow a user"""
    try:
        success = platform.follow_user(user_id, follow_id)
        if not success:
            raise HTTPException(status_code=400, detail="Already following")
        return {"message": f"User {user_id} now follows user {follow_id}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/users/{user_id}/unfollow/{follow_id}")
def unfollow_user(user_id: int, follow_id: int):
    """Unfollow a user"""
    try:
        success = platform.unfollow_user(user_id, follow_id)
        if not success:
            raise HTTPException(status_code=400, detail="Not following")
        return {"message": f"User {user_id} unfollows user {follow_id}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== POST ENDPOINTS ====================

@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate):
    """Create a new post"""
    try:
        new_post = platform.create_post(post.user_id, post.content)
        return {
            "post_id": new_post.post_id,
            "user_id": new_post.user_id,
            "content": new_post.content,
            "like_count": new_post.get_like_count(),
            "comment_count": new_post.get_comment_count(),
            "engagement_score": new_post.get_engagement_score()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/posts/{post_id}/like")
def like_post(post_id: int, user_id: int):
    """Like a post"""
    try:
        success = platform.like_post(user_id, post_id)
        if not success:
            raise HTTPException(status_code=400, detail="Already liked")
        return {"message": "Post liked"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/posts/{post_id}/unlike")
def unlike_post(post_id: int, user_id: int):
    """Unlike a post"""
    try:
        success = platform.unlike_post(user_id, post_id)
        if not success:
            raise HTTPException(status_code=400, detail="Not liked")
        return {"message": "Post unliked"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/posts/{post_id}/comment")
def add_comment(post_id: int, comment: CommentCreate):
    """Add a comment to a post"""
    try:
        new_comment = platform.add_comment(
            comment.user_id,
            post_id,
            comment.content
        )
        return {
            "comment_id": new_comment.comment_id,
            "post_id": new_comment.post_id,
            "user_id": new_comment.user_id,
            "content": new_comment.content
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== FEED ENDPOINT (THE MAIN FEATURE!) ====================

@app.get("/feed/{user_id}")
def get_feed(user_id: int, limit: int = 10):
    """
    Get user's feed - RANKED BY ENGAGEMENT!
    
    This is the MAIN FEATURE of the platform!
    Posts are ranked by: (likes × 2) + (comments × 3)
    """
    try:
        feed_posts = platform.get_user_feed(user_id, limit)
        
        return {
            "user_id": user_id,
            "feed_count": len(feed_posts),
            "posts": [
                {
                    "post_id": post.post_id,
                    "user_id": post.user_id,
                    "content": post.content,
                    "likes": post.get_like_count(),
                    "comments": post.get_comment_count(),
                    "engagement_score": post.get_engagement_score()
                }
                for post in feed_posts
            ]
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== SUGGESTIONS ENDPOINT ====================

@app.get("/suggestions/{user_id}")
def get_suggestions(user_id: int, limit: int = 5):
    """
    Get friend suggestions using BFS algorithm
    (Friends of friends)
    """
    try:
        suggestions = platform.suggest_friends(user_id, limit)
        return {
            "user_id": user_id,
            "suggestions": [
                {
                    "user_id": user.user_id,
                    "username": user.username,
                    "followers": user.get_follower_count()
                }
                for user in suggestions
            ]
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== STATS ENDPOINT ====================

@app.get("/stats")
def get_stats():
    """Get platform statistics"""
    stats = platform.get_platform_stats()
    return {
        "total_users": stats['total_users'],
        "total_posts": stats['total_posts'],
        "total_likes": stats['total_likes'],
        "total_comments": stats['total_comments'],
        "avg_followers": round(stats['avg_followers'], 2)
    }

# ==================== ERROR HANDLERS ====================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors"""
    return HTTPException(status_code=400, detail=str(exc))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
