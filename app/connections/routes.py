"""Routes for managing connections between users."""

from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required
from app.connections import connections  # Import Blueprint directly
from app.auth.models import Student, Alum  # Import your models if necessary


@connections.route('/connections')
# @login_required
def show_connections():
    """Render the connections page."""
    return render_template('connections.html')


@connections.route('/connect', methods=['POST'])
@login_required
def connect():
    """
    Handle connection requests between users.

    Retrieves the receiver's ID and type from the form, validates the inputs,
    and processes the connection request.
    """
    receiver_id = request.form.get('receiver_id')  # ID of the user being connected
    receiver_type = request.form.get('receiver_type')  # Type of user: 'student' or 'alum'

    if receiver_type == 'student':
        receiver = Student.query.get(receiver_id)
    elif receiver_type == 'alum':
        receiver = Alum.query.get(receiver_id)
    else:
        flash('Invalid user type for connection.')
        return redirect(url_for('connections.show_connections'))

    if receiver:
        # Log details of the sender and receiver
        flash(f"Connection request sent to {receiver.first_name} {receiver.last_name}!")
    else:
        flash('User not found.')

    return redirect(url_for('connections.show_connections'))
