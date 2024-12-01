import json
import pytest
from flask import url_for
from app import db
from app.profile.models import Project, Experience, Achievement
from app.auth.models import Student, Alum

def test_create_new_project(client, auth_headers):
    """Test the creation of a new project"""
    data = {
        "title": "New Project",
        "subtitle": "Project Subtitle",
        "description": "Project Description",
        "startDate": "2022-01-01",
        "endDate": "2022-12-31"
    }
    response = client.post("/profile/projects", 
                            data=json.dumps(data), 
                            headers=auth_headers, 
                            content_type="application/json")
    
    assert response.status_code == 201
    assert response.json["title"] == "New Project"

def test_update_existing_experience(client, auth_headers):
    """Test the update of an existing experience"""
    # First, create an experience
    experience = Experience(
        title="Old Experience",
        subtitle="Old Company",
        description="Old Description",
        start_date="2020-01-01",
        end_date="2021-12-31"
    )
    db.session.add(experience)
    db.session.commit()

    data = {
        "title": "Updated Experience",
        "subtitle": "Updated Company",
        "description": "Updated Description",
        "startDate": "2019-01-01",
        "endDate": "2022-12-31"
    }
    response = client.put(f"/profile/experiences/{experience.id}", 
                           data=json.dumps(data), 
                           headers=auth_headers, 
                           content_type="application/json")
    
    assert response.status_code == 200
    assert response.json["title"] == "Updated Experience"