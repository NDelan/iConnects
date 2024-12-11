from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user
from . import connections
from ..auth.models import Student, Alum  # Import your models if necessary
from app import db

@connections.route('/connections')
# @login_required
def show_connections():
    return render_template('connections.html')

@connections.route('/connect', methods=['POST'])
@login_required
def connect():
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
        # Print details of the sender and receiver
        sender = current_user
        print(f"Sender: {sender.first_name} {sender.last_name}, Type: {'Student' if sender.is_student else 'Alum'}")
        print(f"Receiver: {receiver.first_name} {receiver.last_name}, Type: {receiver_type.capitalize()}")

        flash(f"Connection request sent to {receiver.first_name} {receiver.last_name}!")
    else:
        flash('User not found.')

    return redirect(url_for('connections.show_connections'))
