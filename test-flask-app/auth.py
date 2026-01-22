"""
Authentication service for user management and JWT tokens.
"""

import hashlib
import secrets
from typing import Optional, Dict, Any
from database import Database


class AuthService:
    """Handles user authentication and authorization."""
    
    def __init__(self, database: Database):
        self.db = database
        self.secret_key = secrets.token_hex(32)
        self.tokens = {}  # Simple in-memory token store
    
    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        return self.hash_password(password) == password_hash
    
    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user."""
        password_hash = self.hash_password(password)
        
        cursor = self.db.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        
        user_id = cursor.lastrowid
        self.db.close()
        
        return {
            'id': user_id,
            'username': username,
            'email': email
        }
    
    def login(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return token."""
        user = self.db.fetch_one(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        )
        
        if not user or not self.verify_password(password, user['password_hash']):
            return None
        
        # Generate token
        token = secrets.token_hex(32)
        self.tokens[token] = user['id']
        
        return token
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify token and return user."""
        if not token or token not in self.tokens:
            return None
        
        user_id = self.tokens[token]
        user = self.db.fetch_one(
            'SELECT id, username, email FROM users WHERE id = ?',
            (user_id,)
        )
        
        return user
    
    def logout(self, token: str) -> bool:
        """Invalidate a token."""
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False
