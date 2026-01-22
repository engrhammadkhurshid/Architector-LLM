"""
Blog service layer for post and comment operations.
"""

from typing import Optional, List, Dict, Any
from database import Database


class BlogService:
    """Handles blog post and comment operations."""
    
    def __init__(self, database: Database):
        self.db = database
    
    def get_all_posts(self) -> List[Dict[str, Any]]:
        """Get all blog posts with author info."""
        posts = self.db.fetch_all('''
            SELECT p.*, u.username as author_name
            FROM posts p
            JOIN users u ON p.author_id = u.id
            ORDER BY p.created_at DESC
        ''')
        
        # Add comment count
        for post in posts:
            comments = self.db.fetch_all(
                'SELECT COUNT(*) as count FROM comments WHERE post_id = ?',
                (post['id'],)
            )
            post['comment_count'] = comments[0]['count'] if comments else 0
        
        return posts
    
    def get_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific post with comments."""
        post = self.db.fetch_one('''
            SELECT p.*, u.username as author_name
            FROM posts p
            JOIN users u ON p.author_id = u.id
            WHERE p.id = ?
        ''', (post_id,))
        
        if not post:
            return None
        
        # Get comments
        comments = self.db.fetch_all('''
            SELECT c.*, u.username as author_name
            FROM comments c
            JOIN users u ON c.author_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC
        ''', (post_id,))
        
        post['comments'] = comments
        return post
    
    def create_post(self, author_id: int, title: str, content: str) -> Dict[str, Any]:
        """Create a new blog post."""
        cursor = self.db.execute(
            'INSERT INTO posts (author_id, title, content) VALUES (?, ?, ?)',
            (author_id, title, content)
        )
        
        post_id = cursor.lastrowid
        self.db.close()
        
        return self.get_post(post_id)
    
    def update_post(
        self,
        post_id: int,
        author_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Update a blog post."""
        # Check ownership
        post = self.db.fetch_one(
            'SELECT * FROM posts WHERE id = ? AND author_id = ?',
            (post_id, author_id)
        )
        
        if not post:
            return None
        
        updates = []
        params = []
        
        if title:
            updates.append('title = ?')
            params.append(title)
        
        if content:
            updates.append('content = ?')
            params.append(content)
        
        if updates:
            updates.append('updated_at = CURRENT_TIMESTAMP')
            query = f'UPDATE posts SET {", ".join(updates)} WHERE id = ?'
            params.append(post_id)
            
            self.db.execute(query, tuple(params))
            self.db.close()
        
        return self.get_post(post_id)
    
    def delete_post(self, post_id: int, author_id: int) -> bool:
        """Delete a blog post."""
        # Check ownership
        post = self.db.fetch_one(
            'SELECT * FROM posts WHERE id = ? AND author_id = ?',
            (post_id, author_id)
        )
        
        if not post:
            return False
        
        # Delete comments first
        self.db.execute('DELETE FROM comments WHERE post_id = ?', (post_id,))
        
        # Delete post
        self.db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        self.db.close()
        
        return True
    
    def add_comment(self, post_id: int, author_id: int, content: str) -> Dict[str, Any]:
        """Add a comment to a post."""
        cursor = self.db.execute(
            'INSERT INTO comments (post_id, author_id, content) VALUES (?, ?, ?)',
            (post_id, author_id, content)
        )
        
        comment_id = cursor.lastrowid
        self.db.close()
        
        comment = self.db.fetch_one('''
            SELECT c.*, u.username as author_name
            FROM comments c
            JOIN users u ON c.author_id = u.id
            WHERE c.id = ?
        ''', (comment_id,))
        
        return comment
