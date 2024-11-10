from flask import render_template, url_for, redirect, flash, request
from . import posts
from app import db
from app.posts.forms import PostForm
from app.posts.models import Post
from datetime import datetime
import os
from werkzeug.utils import secure_filename

@posts.route('/posts', methods=['GET', 'POST'])
# @login_required
def create_post():
    form = PostForm()

    if request.method == 'POST' and form.validate_on_submit():
        title = request.form.get('title')
        content = request.form.get('content')
        event_name = request.form.get('event_name')
        event_date = request.form.get('event_date')
        event_description = request.form.get('event_description')
        
        # Create a new Post instance
        post = Post(
            title=title,
            content=content,
            timestamp=datetime.utcnow(),
            user_id=None,
            event_name=event_name,
            event_date=event_date,
            event_description=event_description
        )

        # Handle optional image upload
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_filename = secure_filename(image_file.filename)
                image_path = os.path.join('static/uploads/images', image_filename)
                image_file.save(image_path)
                post.image_url = image_path

        # Handle optional video upload
        if 'video' in request.files:
            video_file = request.files['video']
            if video_file.filename != '':
                video_filename = secure_filename(video_file.filename)
                video_path = os.path.join('static/uploads/videos', video_filename)
                video_file.save(video_path)
                post.video_url = video_path

        # Save post to the database
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for('posts.create_post'))

    # Fetch and display existing posts, ordered by timestamp
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('post.html', form=form, posts=posts)
    # return render_template('post.html')