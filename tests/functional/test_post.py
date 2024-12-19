"""
test for post.py
"""
import pytest
from app.posts.models import Post

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

def test_create_post(test_client, new_post_data):
    """Test the creation of a post."""
    test_client.post('/signin', data={
        'username': 'denutak',
        'password': '11111111'
    }, follow_redirects=True)

    response = test_client.post('/posts', data={
        'title': new_post_data["title"],
        'content': new_post_data["content"],
        'event_name': new_post_data["event_name"],
        'event_description': new_post_data["event_description"],
        'event_date': new_post_data["event_date"],
    }, content_type='multipart/form-data', follow_redirects=True)
    
    assert response.status_code == 200

    post = Post.query.filter_by(title=new_post_data["title"]).first()
    assert post is not None
    assert post.content == new_post_data["content"]

def test_list_posts(test_client):
    """Test listing all posts."""
    test_client.post('/signin', data={
        'username': 'denutak',
        'password': '11111111'
    }, follow_redirects=True)
    response = test_client.get('/posts')
    assert response.status_code == 200

def test_post_not_found(test_client):
    """Test accessing a non-existent post."""
    test_client.post('/signin', data={
        'username': 'denutak',
        'password': '11111111'
    }, follow_redirects=True)

    response = test_client.get('/posts/9999')
    assert response.status_code == 404

def test_serve_media_not_found(test_client):
    """Test serving a non-existing media."""
    test_client.post('/signin', data={
        'username': 'denutak',
        'password': '11111111'
    }, follow_redirects=True)
    response = test_client.get('/media/1/<string:media_type>')
    assert response.status_code == 404
