from flask import render_template, url_for, redirect, flash, request
from . import posts
from app import db
from app.posts.models import Post
from flask_login import current_user, login_required
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask import Response

@posts.route('/posts', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        event_name = request.form.get('event_name')
        event_description = request.form.get('event_description')
        event_date_str = request.form.get('event_date')
        event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date() if event_date_str else None

        post = Post(
            title=title,
            content=content,
            timestamp=datetime.utcnow(),
            user_id=current_user.get_id(),
            event_name=event_name,
            event_date=event_date,
            event_description=event_description
        )

        image = request.files.get('image')
        if image:
            post.image_data = image.read()
            post.image_content_type = image.content_type

        video = request.files.get('video')
        if video:
            post.video_data = video.read()
            post.video_content_type = video.content_type

        db.session.add(post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for('posts.create_post'))

    all_posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('post.html', posts=all_posts)

@posts.route('/media/<int:post_id>/<string:media_type>')
def serve_media(post_id, media_type):
    post = Post.query.get_or_404(post_id)
    if media_type == "image" and post.image_data:
        return Response(post.image_data, mimetype=post.image_content_type)
    elif media_type == "video" and post.video_data:
        return Response(post.video_data, mimetype=post.video_content_type)
    return "Media not found", 404