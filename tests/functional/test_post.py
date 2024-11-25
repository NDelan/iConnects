import pytest
from app.posts.models import Post
from app import db
from datetime import datetime

@pytest.fixture
def new_post_data():
    """Fixture for creating post data."""
    return {
        "title": "Test Post",
        "content": "This is a test post.",
        "event_name": "Test Event",
        "event_description": "Event Description",
        "event_date": "2024-11-24",
    }

def test_create_post(test_client, new_post_data, alum_user):
    """Test the creation of a post."""
    with test_client:
        test_client.post('/login', data={
            'email': alum_user.email,
            'password': 'password123'
        }, follow_redirects=True)
        
        response = test_client.post('/posts', data={
            'title': new_post_data["title"],
            'content': new_post_data["content"],
            'event_name': new_post_data["event_name"],
            'event_description': new_post_data["event_description"],
            'event_date': new_post_data["event_date"],
        }, content_type='multipart/form-data', follow_redirects=True)
        
        assert response.status_code == 200
        assert b"Post created successfully!" in response.data
        
        post = Post.query.filter_by(title=new_post_data["title"]).first()
        assert post is not None
        assert post.content == new_post_data["content"]

def test_list_posts(test_client):
    """Test listing all posts."""
    response = test_client.get('/posts')
    assert response.status_code == 200
    assert b"All Posts" in response.data

def test_serve_media_not_found(test_client, alum_user):
    """Test serving a non-existing media."""
    response = test_client.get('/media/9999/image')
    assert response.status_code == 404