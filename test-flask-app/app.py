"""
Simple Flask Blog Application
Demonstrates a typical web application structure with models, routes, and services.
"""

from flask import Flask, jsonify, request
from database import Database
from auth import AuthService
from blog_service import BlogService

app = Flask(__name__)
db = Database('blog.db')
auth_service = AuthService(db)
blog_service = BlogService(db)


@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.json
    user = auth_service.register(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    return jsonify(user), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user and return token."""
    data = request.json
    token = auth_service.login(
        username=data['username'],
        password=data['password']
    )
    return jsonify({'token': token}), 200


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all blog posts."""
    posts = blog_service.get_all_posts()
    return jsonify(posts), 200


@app.route('/api/posts', methods=['POST'])
def create_post():
    """Create a new blog post."""
    data = request.json
    token = request.headers.get('Authorization')
    
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    post = blog_service.create_post(
        author_id=user['id'],
        title=data['title'],
        content=data['content']
    )
    return jsonify(post), 201


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific blog post."""
    post = blog_service.get_post(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a blog post."""
    data = request.json
    token = request.headers.get('Authorization')
    
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    post = blog_service.update_post(
        post_id=post_id,
        author_id=user['id'],
        title=data.get('title'),
        content=data.get('content')
    )
    
    if not post:
        return jsonify({'error': 'Post not found or unauthorized'}), 404
    
    return jsonify(post), 200


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a blog post."""
    token = request.headers.get('Authorization')
    
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    success = blog_service.delete_post(post_id, user['id'])
    if not success:
        return jsonify({'error': 'Post not found or unauthorized'}), 404
    
    return '', 204


@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    """Add a comment to a post."""
    data = request.json
    token = request.headers.get('Authorization')
    
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    comment = blog_service.add_comment(
        post_id=post_id,
        author_id=user['id'],
        content=data['content']
    )
    
    return jsonify(comment), 201


if __name__ == '__main__':
    db.initialize()
    app.run(debug=True, port=5000)
