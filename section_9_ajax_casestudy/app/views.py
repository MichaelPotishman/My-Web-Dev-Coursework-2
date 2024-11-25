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
            
            profile_pic = post.user.profile_picture if post.user.profile_picture else 'default.jpg'
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
    return render_template('feed.html', theme=theme, posts=posts_dict, liked_posts = liked_posts, user_id=current_user.id, post_id = post_id)

@app.route('/search', methods=['GET'])
def search_page():
    user_posts = models.Posts.query.join(models.User, models.Posts.user_id == models.User.id).join(models.PostHashtag, models.Posts.post_id == models.PostHashtag.post_id).join(models.Hashtags, models.PostHashtag.hashtag_id == models.Hashtags.id).order_by(models.Posts.post_id.desc()).all()
    theme=request.cookies.get('theme')
    return render_template('search.html', posts = user_posts, theme=theme)
    

@app.route("/search/<string:search_text>", methods=["GET"])
@login_required
def search(search_text):
    filtered_posts = (
        models.Posts.query
        .outerjoin(models.PostHashtag, models.Posts.post_id == models.PostHashtag.post_id)
        .outerjoin(models.Hashtags, models.PostHashtag.hashtag_id == models.Hashtags.id)
        .filter(
            (models.Posts.content.ilike(f"%{search_text}%")) | 
            (models.Hashtags.name.ilike(f"%{search_text}%"))
        )
        .distinct()
        .all()
    )
    
    print(f"Filtered posts count: {len(filtered_posts)}")
    
    liked_posts = {}
    posts_data = {}
    
    for post in filtered_posts:
        post_id = post.post_id
        posts_data[post_id] = {
            "user_id": post.user_id,
            "username": post.user.username,
            "content": post.content,
            "profile_picture": post.user.profile_picture,
            "hashtags": [tag.name for tag in post.hashtags],
            "upvotes": post.upvotes,
            "image": post.image
        }
        
        existing_like = models.Likes.query.filter_by(user_id=current_user.id, post_id=post_id).first()
        liked_posts[post_id] = bool(existing_like)
    
    print("Posts Data:", posts_data)
    return render_template("_search_results.html", posts=posts_data, liked_posts=liked_posts)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    theme = request.cookies.get('theme')

    # Debug: Print all files in request
    print("Files in request:", request.files)
    print("Form data:", request.form)

    if form.validate_on_submit():
        hashtags = set()
        content = form.content.data
        raw_hashtags = form.hashtags.data
        user_id = current_user.id
        
        
        filename = None
        

        if 'image_or_video' in request.files:
            file = request.files['image_or_video']
            print(f"Received file: {file.filename}")
            
            if file.filename == '':
                print("No filename provided")
                filename = None
            else:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

                file.save(file_path)
                
   
        # Create and add the new post with the image filename
        new_post = models.Posts(
            content=content,
            user_id=user_id,
            image=filename
        )
        
        
        db.session.add(new_post)
        db.session.flush()

        # Process hashtags (rest of the code remains the same)
        raw_hashtags = raw_hashtags.replace(',', ' ')
        words = raw_hashtags.split()

        for word in words:
            potential_tags = word.split('#')
            for tag in potential_tags:
                tag = tag.strip()
                if tag:
                    hashtags.add(tag)

        for hashtag_name in hashtags:
            hashtag = models.Hashtags.query.filter_by(name=hashtag_name).first()
            if not hashtag:
                hashtag = models.Hashtags(name=hashtag_name)
                db.session.add(hashtag)
                db.session.flush()

            post_hashtag = models.PostHashtag(post_id=new_post.post_id, hashtag_id=hashtag.id)
            db.session.add(post_hashtag)
            
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect('/feed')

    return render_template('post.html', theme=theme, form=form, user_id=current_user.id)

# Add this helper function to check file extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    return render_template('profile.html', user=user, posts=user_posts_dict, theme=theme, user_id=current_user.id)

@app.route('/hashtag-profile/<string:hashtag_name>', methods=['GET', 'POST'])
@login_required
def hashtag_profile(hashtag_name):
    hashtag = hashtag_name  # 'hashtag' is being passed to the template
    posts_with_hashtag = models.Posts.query \
        .join(models.PostHashtag, models.Posts.post_id == models.PostHashtag.post_id) \
        .join(models.Hashtags, models.PostHashtag.hashtag_id == models.Hashtags.id) \
        .filter(models.Hashtags.name == hashtag_name) \
        .order_by(models.Posts.post_id.desc()).all()

    posts_dict = {}
    for post in posts_with_hashtag:
        image = post.image if post.image else ''
        post_id = post.post_id
        posts_dict[post_id] = {
            'content': post.content,
            'username': post.user.username,
            'hashtags': hashtag, 
            'upvotes': post.upvotes,
            'user_id': post.user_id,
            'image': image
        }

    theme = request.cookies.get('theme')
    return render_template('hashtag_profile.html', theme=theme, posts=posts_dict, hashtag=hashtag_name)

@app.route('/edit/<int:post_id>', methods=['GET','POST'])
@login_required
def edit_post(post_id):
    theme = request.cookies.get('theme')
    post = models.Posts.query.get(post_id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        if not form.content.data or not form.hashtags.data:
            flash("Content and Hashtags are required fields")
            return render_template('feed.html', theme=theme)
        
        # place the data already in the database on the form so users can edit
        post.content = form.content.data
        post.image_or_video = form.image_or_video.data
        post.hashtags = form.hashtags.data
        
        flash("Successfully updated your post!")
        db.session.commit()
        
    return render_template('edit.html', form=form, theme=theme)

# Flask routes
@app.route('/profile/<username>/posts')
def get_user_posts(username):
    user = models.User.query.filter_by(username=username).first()
    posts = models.Posts.query.filter_by(user_id=user.id).order_by(models.Posts.timestamp.desc()).all()
    
    return render_template('_posts.html', posts=posts)  # Note the underscore prefix for partial template

@app.route('/profile/<username>/likes')
def get_user_likes(username):
    user = models.User.query.filter_by(username=username).first_or_404()
    liked_posts = models.Posts.query.join(models.Likes).filter(models.Likes.user_id == user.id).all()
    
    return render_template('_likes.html', posts=liked_posts)
    



@app.route('/delete_account/<int:user_id>', methods=['POST'])
@login_required
def delete_account(user_id):
    user = models.User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')



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
