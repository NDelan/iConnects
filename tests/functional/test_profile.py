import pytest
from app.profile.models import Project, Experience, Achievement
from app import db
import json

@pytest.fixture
def new_project_data():
    """Fixture for creating project data."""
    return {
        "title": "Test Project",
        "subtitle": "Project Subtitle",
        "description": "This is a test project.",
        "startDate": "2024-01-01",
        "endDate": None,
    }

@pytest.fixture
def new_experience_data():
    """Fixture for creating experience data."""
    return {
        "title": "Test Experience",
        "subtitle": "Company Name",
        "description": "Worked on something impactful.",
        "startDate": "2023-01-01",
        "endDate": "2023-12-31",
    }

@pytest.fixture
def new_achievement_data():
    """Fixture for creating achievement data."""
    return {
        "title": "Hackathon Winner",
        "subtitle": "National Hackathon",
        "description": "Won the first place in a prestigious competition.",
        "startDate": "2024-11-24",
        "endDate": None,
    }

# New fixture to handle user signup
@pytest.fixture
def signup_user(test_client):
    """Fixture for signing up a user."""
    # Sign up a new user
    test_client.post('/signup', data={
        'username': 'denutak',
        'password': '11111111',
        'email': 'denutak@example.com',
        'first_name': 'Delanyo',
        'last_name': 'Nutakor',
    }, follow_redirects=True)
    
    # Return user data for use in other tests
    return {
        'username': 'denutak',
        'password': '11111111'
    }

def test_view_profile_page(test_client, signup_user):
    """Test viewing the profile page."""
    # Use the signup_user fixture to sign in
    test_client.post('/signin', data={
        'username': signup_user['username'],
        'password': signup_user['password']
    }, follow_redirects=True)

    response = test_client.get('/profile')
    assert response.status_code == 200

    assert b"Profile Page" in response.data
    assert b"Achievements" in response.data
    assert b"Experience" in response.data
    assert b"Projects" in response.data

def test_add_project(test_client, new_project_data):
    """Test adding a project."""
    test_client.post('/signin', data={
        'username': 'denutak',
        'password': '11111111'
    }, follow_redirects=True)

    response = test_client.post('/api/profile/projects', 
                                 data=json.dumps(new_project_data), 
                                 content_type='application/json', 
                                 follow_redirects=True)
    assert response.status_code == 201

    project = Project.query.filter_by(title=new_project_data["title"]).first()
    assert project is not None
    assert project.description == new_project_data["description"]
    assert project.is_current is True

def test_add_experience(test_client, new_experience_data):
    """Test adding an experience."""
    test_client.post('/signin', data={
        'username': 'denutak',
        'password': '11111111'
    }, follow_redirects=True)

    response = test_client.post('/api/profile/experiences', 
                                 data=json.dumps(new_experience_data), 
                                 content_type='application/json', 
                                 follow_redirects=True)
    assert response.status_code == 201

    experience = Experience.query.filter_by(title=new_experience_data["title"]).first()
    assert experience is not None
    assert experience.subtitle == new_experience_data["subtitle"]

def test_add_achievement(test_client, new_achievement_data):
    """Test adding an achievement."""
    test_client.post('/signin', data={
        'username': 'denutak',
        'password': '11111111'
    }, follow_redirects=True)

    response = test_client.post('/api/profile/achievements', 
                                 data=json.dumps(new_achievement_data), 
                                 content_type='application/json', 
                                 follow_redirects=True)
    assert response.status_code == 201

    achievement = Achievement.query.filter_by(title=new_achievement_data["title"]).first()
    assert achievement is not None
    assert achievement.subtitle == new_achievement_data["subtitle"]

def test_profile_item_not_found(test_client):
    """Test accessing a non-existent project."""
    test_client.post('/signin', data={
        'username': 'denutak',
        'password': '11111111'
    }, follow_redirects=True)

    response = test_client.get('/profile/projects/9999')
    assert response.status_code == 404

def test_delete_project(test_client, new_project_data):
    """Test deleting a project."""
    test_client.post('/signin', data={
        'username': 'denutak',
        'password': '11111111'
    }, follow_redirects=True)

    # Add a project first
    add_response = test_client.post('/api/profile/projects', 
                                    data=json.dumps(new_project_data), 
                                    content_type='application/json', 
                                    follow_redirects=True)
    assert add_response.status_code == 201

    project = Project.query.filter_by(title=new_project_data["title"]).first()
    assert project is not None

    # Delete the project
    delete_response = test_client.delete(f'/api/profile/projects/{project.id}', follow_redirects=True)
    assert delete_response.status_code == 200
    assert Project.query.get(project.id) is None

def test_add_project_invalid_data(test_client):
    """Test adding a project with invalid data."""
    test_client.post('/signin', data={
        'username': 'denutak',
        'password': '11111111'
    }, follow_redirects=True)

    invalid_data = {"title": "", "description": ""}  # Missing required fields
    response = test_client.post('/api/profile/projects', 
                                 data=json.dumps(invalid_data), 
                                 content_type='application/json', 
                                 follow_redirects=True)
    assert response.status_code == 400

def test_user_isolation(test_client, signup_user):
    """Test that one user's data is not accessible by another user."""
    # Create data for User A
    test_client.post('/signin', data={
        'username': signup_user['username'],
        'password': signup_user['password']
    }, follow_redirects=True)

    new_project = {"title": "User A Project", "description": "Test"}
    test_client.post('/api/profile/projects', 
                     data=json.dumps(new_project), 
                     content_type='application/json')

    # Sign out and log in as a different user
    test_client.get('/signout', follow_redirects=True)
    test_client.post('/signup', data={
        'username': 'userB',
        'password': 'passwordB',
        'email': 'userB@example.com',
        'first_name': 'User',
        'last_name': 'B'
    }, follow_redirects=True)

    # Ensure User B cannot see User A's project
    response = test_client.get('/profile/projects')
    assert b"User A Project" not in response.data


def test_update_project(test_client, new_project_data):
    """Test updating a project."""
    test_client.post('/signin', data={
        'username': 'denutak',
        'password': '11111111'
    }, follow_redirects=True)

    # Add a project
    add_response = test_client.post('/api/profile/projects', 
                                    data=json.dumps(new_project_data), 
                                    content_type='application/json', 
                                    follow_redirects=True)
    assert add_response.status_code == 201

    project = Project.query.filter_by(title=new_project_data["title"]).first()
    assert project is not None

    # Update the project
    updated_data = {"title": "Updated Project Title"}
    update_response = test_client.put(f'/api/profile/projects/{project.id}', 
                                      data=json.dumps(updated_data), 
                                      content_type='application/json', 
                                      follow_redirects=True)
    assert update_response.status_code == 200
    updated_project = Project.query.get(project.id)
    assert updated_project.title == "Updated Project Title"
