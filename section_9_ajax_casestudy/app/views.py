from app import app, models, db
from flask import render_template, flash, request, redirect
from .forms import LoginForm, RegisterForm, PostForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

import os

UPLOAD_FOLDER = 'app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 


import json

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logout_user()
        print("Logged out existing user")
    
    theme = request.cookies.get('theme')
    print(f"theme = {theme}")
    form = LoginForm()
    if form.validate_on_submit():

        user = models.User.query.filter_by(username=form.username.data).first()
        print(f"USERNAME = {user}")
        if user and user.password == form.password.data:  # Ideally, hash and check passwords
            login_user(user)
            return redirect('/feed')  # Redirect to the homepage or dashboard
        else:
            flash("Invalid username or password.")
    
    return render_template('home.html', form=form, title="Login / Register", theme=theme)

@app.route('/register', methods=['GET','POST'])
def register():
    theme = request.cookies.get('theme')
    form = RegisterForm()
    if form.validate_on_submit():
        # Handle registration logic
        profile_picture = request.files['profile_picture']
        
        if profile_picture.filename == '':
            filename = 'default.png'  # User did not upload a file
        elif profile_picture:
            filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return "Invalid file type"
            
    
        new_user = models.User(username=form.username.data, password=form.password.data, email=form.email.data, date_of_birth=form.date_of_birth.data, profile_picture=filename)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Hello {form.username.data}, you have been successfully registered!")
        return redirect('/')

    return render_template('register.html', form=form, title="Login / Register", theme=theme)

        
@app.route('/feed', methods=['GET','POST'])
@login_required
def feed():
    # Join User table to Post, then Post to PostHshtag, then PostHashtag to Hashtag
    user_posts = models.Posts.query.join(models.User, models.Posts.user_id == models.User.id).join(models.PostHashtag, models.Posts.post_id == models.PostHashtag.post_id).join(models.Hashtags, models.PostHashtag.hashtag_id == models.Hashtags.id).order_by(models.Posts.post_id.desc()).all()

    posts_dict = {}
    liked_posts = {}
    for post in user_posts:
        post_id = post.post_id
        if post.post_id not in posts_dict:
            
            profile_pic = post.user.profile_picture if post.user.profile_picture else 'default.png'
            image = post.image if post.image else ''
            
            posts_dict[post_id] = {'content' : post.content,
                                   'username': post.user.username,
                                   'hashtags': [],
                                   'upvotes': post.upvotes,
                                   'user_id': post.user_id,
                                   'profile_picture': profile_pic,
                                   'image': image}
        for hashtag in post.hashtags:
            posts_dict[post_id]['hashtags'].append(hashtag.name)
            
        existing_like = models.Likes.query.filter_by(user_id=current_user.id, post_id=post_id).first()
        if existing_like:
            print("FOR POST :", post_id, "EXISTING LIKE: TRUE")
        liked_posts[post_id] = bool(existing_like)
        

    theme = request.cookies.get('theme')
    return render_template('feed.html', theme=theme, posts=posts_dict, liked_posts = liked_posts, user_id=current_user.id)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    theme = request.cookies.get('theme')

    if form.validate_on_submit():
        hashtags = set()
        content = form.content.data
        raw_hashtags = form.hashtags.data  # e.g., #1 #fdf #fdfsfdsfeewf
        user_id = current_user.id
        
        # get image user gave
        image = request.files['image']
        
        if image.filename == '':
            filename = ''  # User did not upload a file
        elif image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return "Invalid file type"

        # Create and add a new post
        new_post = models.Posts(content=content, user_id=user_id, image=filename)
        db.session.add(new_post)
        db.session.flush()  # Ensure the new post is saved, and we get its ID

        # Process hashtags
        raw_hashtags = raw_hashtags.replace(',', ' ')
        words = raw_hashtags.split()

        for word in words:
            potential_tags = word.split('#')
            for tag in potential_tags:
                tag = tag.strip()
                if tag:
                    hashtags.add(tag)

        for hashtag_name in hashtags:
            # Check if the hashtag exists in the database
            hashtag = models.Hashtags.query.filter_by(name=hashtag_name).first()
            if not hashtag:
                # Add new hashtag to the database
                hashtag = models.Hashtags(name=hashtag_name)
                db.session.add(hashtag)
                db.session.flush()  # Ensure the new hashtag is saved, and we get its ID

            # Create a link between the post and the hashtag
            post_hashtag = models.PostHashtag(post_id=new_post.post_id, hashtag_id=hashtag.id)
            db.session.add(post_hashtag) 

        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect('/feed') # Assuming 'feed' is the route for viewing posts

    return render_template('post.html', theme=theme, form=form, user_id=current_user.id)

from flask import request, jsonify
import json

@app.route('/vote', methods=['POST'])
@login_required
def vote():
    data = json.loads(request.data)
    post_id = int(data.get('post_id'))
    print("Post ID = ", post_id)
    
    
    # this looks through likes table and sees if current post id has been liked already by the current user
    existing_like = models.Likes.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    
    post = models.Posts.query.get(post_id)
    

    if post is None:
        return json.dumps({'status': 'error', 'message': f'Post with ID {post_id} not found'}), 404

    # Initialize upvotes to 0 if None
    if post.upvotes is None:
        post.upvotes = 0

    if data.get('vote_type'):
        if existing_like:
            print("EXISTING LIKE")
            db.session.delete(existing_like)
            post.upvotes -= 1
        else:
            new_like = models.Likes(user_id=current_user.id, post_id=post_id)
            db.session.add(new_like)
            post.upvotes += 1
            
    db.session.commit()
    return json.dumps({'status':'OK', 'upvotes': post.upvotes})

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = models.Posts.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect('/feed')

@app.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def profile(user_id):
    # Get only specific posts from that user and show them with the information on it
    user = models.User.query.get(user_id)
    users_posts = models.Posts.query.filter_by(user_id=user_id).order_by(models.Posts.post_id.desc()).all()
    
    user_posts_dict = {}
    for post in users_posts:
        post_id = post.post_id
        if post.post_id not in user_posts_dict:
            user_posts_dict[post_id] = { 
                'content': post.content, 
                'username': user.username, 
                'hashtags': [], 
                'upvotes': post.upvotes,
                'user_id': current_user.id
                }
            for hashtag in post.hashtags:
                user_posts_dict[post_id]['hashtags'].append(hashtag.name)
            
    theme = request.cookies.get('theme')
    return render_template('profile.html', user=user, posts=user_posts_dict, theme=theme)

# @app.route('/hashtag-profile/<int:hashtag_id>', methods=['GET','POST'])
# @login_required
# def hashtag_profile(hashtag_id):
#     posts_with_hashtag = models.Post.query.join(models.PostHashtag, models.Posts.post_id == models.PostHashtag.post_id).join(models.Hashtags, models.PostHashtag.hashtag_id == models.Hashtags.id).filter_by(models.Hashtags.id == hashtag_id).order_by(models.Posts.post_id.desc()).all()
#     filtered_posts = []
#     for post in posts_with_hashtag:
#         filtered_posts.append({
#             'content': post.content,
#             'username': post.user.username,
#             'hashtags': [h.name for h in post.hashtags],
#             'upvotes': post.upvotes,
#             'user_id': post.user_id
#         })
        
#     theme = request.cookies.get('theme')
#     return render_template('hashtag_profile.html', theme=theme, posts=filtered_posts)
    

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')
    
# @app.route('/livesearch', methods=['POST'])
# def livesearch():
#     search_hashtag = request.form['query'].lower().strip('#')

#     # Retrieve posts, join with User, PostHashtag, and Hashtags to get the required data
#     user_posts = models.Posts.query \
#         .join(models.User, models.Posts.user_id == models.User.id) \
#         .join(models.PostHashtag, models.Posts.post_id == models.PostHashtag.post_id) \
#         .join(models.Hashtags, models.PostHashtag.hashtag_id == models.Hashtags.id) \
#         .order_by(models.Posts.post_id.desc()).all()
    
#     filtered_posts = []
#     liked_posts = {}

#     # Loop through user_posts (which is a list of SQLAlchemy model objects)
#     for post in user_posts:
#         # Access the hashtags and ensure case-insensitivity
#         hashtags = [h.name.lower() for h in post.hashtags]  # Assuming the 'Hashtags' model has a 'name' field
        
#         # Check if the search term is in any of the hashtags
#         if search_hashtag in ' '.join(hashtags):
#             filtered_posts.append(post)
            
#         # Check if the current user has liked this post
#         existing_like = models.Likes.query.filter_by(user_id=current_user.id, post_id=post.post_id).first()
#         liked_posts[post.post_id] = bool(existing_like)

#     # Render the filtered posts with liked status
#     return render_template('feed-content.html', 
#                            posts=filtered_posts, 
#                            liked_posts=liked_posts,
#                            current_user=current_user)
