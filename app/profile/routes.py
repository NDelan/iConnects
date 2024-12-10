from flask import render_template, url_for, redirect, Blueprint, request, jsonify, current_app, Response
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.profile.models import Project, Experience, Achievement
from app.auth.models import Student, Alum
from . import profile
from datetime import datetime

@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    """Render the profile page."""
    FIRST = current_user.first_name
    LAST = current_user.last_name
    return render_template('profile.html', firstName=FIRST, lastName=LAST)

def parse_date(date_str):
    """Convert date string to datetime object."""
    if not date_str or date_str == 'Present':
        return None
    return datetime.strptime(date_str, '%Y-%m-%d')

@profile.route('/profile/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    """Update the user's profile, including profile picture."""
    user = current_user
    name = request.form.get('name')
    title = request.form.get('title')
    profile_picture = request.files.get('profile_picture')


    if name:
        user.first_name, user.last_name = name.split(" ", 1) if " " in name else (name, user.last_name)
    if title:
        user.headline = title

    if profile_picture:
        user.profile_picture_data = profile_picture.read()
        user.profile_picture_content_type = profile_picture.content_type

    try:
        db.session.commit()
        return render_template('profile.html')
    except Exception as e:
        current_app.logger.error(f"Error updating profile: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Could not update profile'}), 400

@profile.route('/profile-picture/<int:user_id>')
def serve_profile_picture(user_id):
    """Serve the profile picture for a user."""
    if current_user.__tablename__== 'alum':
        user_id = current_user.alum_id
        user = Alum.query.get_or_404(user_id)
    else:
        user_id = current_user.student_id
        user = Student.query.get_or_404(user_id)
    if user.profile_picture_data:
        return Response(user.profile_picture_data, mimetype=user.profile_picture_content_type)
    return redirect(url_for('static', filename='images/profile.jpg'))

@profile.route('/api/profile/<section>', methods=['POST'])
@login_required
def add_profile_section(section):
    """Add a new item to profile section (projects, experiences, achievements)."""
    data = request.json
    models = {'projects': Project, 'experiences': Experience, 'achievements': Achievement}

    if section not in models:
        return jsonify({'error': 'Invalid section'}), 400

    try:
        if not data.get('title') or not data.get('description'):
            return jsonify({'error': 'Title and description are required'}), 400

        new_item = models[section](
            title=data['title'],
            subtitle=data.get('subtitle', ''),
            description=data.get('description', ''),
            start_date=parse_date(data.get('startDate')),
            end_date=parse_date(data.get('endDate')),
            is_current=data.get('endDate') is None
        )

        if hasattr(current_user, 'student_id'):
            new_item.student_id = current_user.student_id
        else:
            new_item.alum_id = current_user.alum_id

        db.session.add(new_item)
        db.session.commit()

        return jsonify({
            'id': new_item.id,
            'title': new_item.title,
            'subtitle': new_item.subtitle,
            'description': new_item.description,
            'startDate': new_item.start_date.strftime('%Y-%m-%d') if new_item.start_date else None,
            'endDate': 'Present' if new_item.is_current else (
                new_item.end_date.strftime('%Y-%m-%d') if new_item.end_date else None)
        }), 201

    except Exception as e:
        current_app.logger.error(f"Error adding {section} item: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Could not add item'}), 400

@profile.route('/api/profile/<section>/<int:item_id>', methods=['PUT'])
@login_required
def update_profile_section(section, item_id):
    """Update an existing profile section item."""
    data = request.json
    models = {'projects': Project, 'experiences': Experience, 'achievements': Achievement}

    if section not in models:
        return jsonify({'error': 'Invalid section'}), 400

    try:
        item = models[section].query.get_or_404(item_id)
        if (hasattr(current_user, 'student_id') and item.student_id != current_user.student_id) or \
           (hasattr(current_user, 'alum_id') and item.alum_id != current_user.alum_id):
            return jsonify({'error': 'Unauthorized'}), 403

        item.title = data.get('title', item.title)
        item.subtitle = data.get('subtitle', item.subtitle)
        item.description = data.get('description', item.description)
        item.start_date = parse_date(data.get('startDate')) or item.start_date
        item.end_date = parse_date(data.get('endDate')) or item.end_date
        item.is_current = data.get('endDate') is None

        db.session.commit()

        return jsonify({
            'id': item.id,
            'title': item.title,
            'subtitle': item.subtitle,
            'description': item.description,
            'startDate': item.start_date.strftime('%Y-%m-%d') if item.start_date else None,
            'endDate': 'Present' if item.is_current else (
                item.end_date.strftime('%Y-%m-%d') if item.end_date else None)
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error updating {section} item: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Could not update item'}), 400

@profile.route('/api/profile/<section>/<int:item_id>', methods=['DELETE'])
@login_required
def delete_profile_section(section, item_id):
    """Delete a profile section item."""
    models = {'projects': Project, 'experiences': Experience, 'achievements': Achievement}

    if section not in models:
        return jsonify({'error': 'Invalid section'}), 400

    try:
        item = models[section].query.get_or_404(item_id)
        if (hasattr(current_user, 'student_id') and item.student_id != current_user.student_id) or \
           (hasattr(current_user, 'alum_id') and item.alum_id != current_user.alum_id):
            return jsonify({'error': 'Unauthorized'}), 403

        db.session.delete(item)
        db.session.commit()

        return jsonify({'message': 'Item deleted successfully'})

    except Exception as e:
        current_app.logger.error(f"Error deleting {section} item: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Could not delete item'}), 500

@profile.route('/api/profile/<section>', methods=['GET'])
@login_required
def get_profile_section(section):
    """Get all items for a profile section."""
    models = {'projects': Project, 'experiences': Experience, 'achievements': Achievement}

    if section not in models:
        return jsonify({'error': 'Invalid section'}), 400

    try:
        if hasattr(current_user, 'student_id'):
            items = models[section].query.filter_by(student_id=current_user.student_id).all()
        else:
            items = models[section].query.filter_by(alum_id=current_user.alum_id).all()

        return jsonify([{
            'id': item.id,
            'title': item.title,
            'subtitle': item.subtitle,
            'description': item.description,
            'startDate': item.start_date.strftime('%Y-%m-%d') if item.start_date else None,
            'endDate': 'Present' if item.is_current else (
                item.end_date.strftime('%Y-%m-%d') if item.end_date else None)
        } for item in items])

    except Exception as e:
        current_app.logger.error(f"Error fetching {section} items: {str(e)}")
        return jsonify({'error': 'Could not fetch items'}), 500