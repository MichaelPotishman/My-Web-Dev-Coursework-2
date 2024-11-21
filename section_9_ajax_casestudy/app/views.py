from app import app, models, db
from flask import render_template, flash, request, redirect
from .forms import IdeaForm, LoginForm, RegisterForm, PostForm
from flask_login import login_user, logout_user, login_required, current_user



import json




# @app.route('/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()

#     if form.validate_on_submit():
#         action = request.form.get('action')  # Get the action value from the form submission
#         print("Action: ", action)

#         if action == 'registering':
#             # Handle registration logic
#             new_user = models.User(username=form.username.data, password=form.password.data)
#             db.session.add(new_user)
#             db.session.commit()
#             flash(f"Hello {form.username.data}, you have been successfully registered!")
        
#         elif action == 'logging-in':
#             # Handle login logic
#             user = models.User.query.filter_by(username=form.username.data).first()
#             if user and user.password == form.password.data:  # Ideally, hash and check passwords
#                 login_user(user)
#                 flash("Login Successful!")
#                 return redirect(url_for('index'))  # Redirect to the homepage or dashboard
#             else:
#                 flash("Invalid username or password.")
    
#     return render_template('home.html', form=form, title="Login / Register")

# @app.route('/', methods=['GET','POST'])
# def home():
#     form = LoginForm()
#     return render_template('home.html', form=form, title="Login / Register")

@app.route('/', methods=['GET', 'POST'])
def login():
    
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
        new_user = models.User(username=form.username.data, password=form.password.data, email=form.email.data, date_of_birth=form.date_of_birth.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Hello {form.username.data}, you have been successfully registered!")
        return redirect('/')

    return render_template('register.html', form=form, title="Login / Register", theme=theme)

        
@app.route('/feed', methods=['GET','POST'])
def feed():
    # Join User table to Post, then Post to PostHshtag, then PostHashtag to Hashtag
    user_posts = models.Posts.query.join(models.User, models.Posts.user_id == models.User.id).join(models.PostHashtag, models.Posts.post_id == models.PostHashtag.post_id).join(models.Hashtags, models.PostHashtag.hashtag_id == models.Hashtags.id).order_by(models.Posts.post_id.desc()).all()

    posts_dict = {}
    for post in user_posts:
        post_id = post.post_id
        if post.post_id not in posts_dict:
            posts_dict[post_id] = {'content' : post.content, 'username': post.user.username, 'hashtags': [], 'upvotes': post.upvotes}
        for hashtag in post.hashtags:
            posts_dict[post_id]['hashtags'].append(hashtag.name)
        

    theme = request.cookies.get('theme')
    return render_template('feed.html', theme=theme, posts=posts_dict)

@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    theme = request.cookies.get('theme')

    if form.validate_on_submit():
        hashtags = set()
        content = form.content.data
        raw_hashtags = form.hashtags.data  # e.g., #1 #fdf #fdfsfdsfeewf
        user_id = current_user.id

        # Create and add a new post
        new_post = models.Posts(content=content, user_id=user_id)
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

    return render_template('post.html', theme=theme, form=form)



from flask import request, jsonify
import json

@app.route('/vote', methods=['POST'])
def vote():
    try:
        # Parse incoming JSON data
        data = json.loads(request.data)
        post_id = int(data.get('post_id'))
        vote_type = data.get('vote_type')

        # Query the database for the relevant post
        post = models.Post.query.get(post_id)  # Adjust to match your model name

        if not post:
            return jsonify({'error': 'Post not found'}), 404

        # Update vote count based on vote type
        if vote_type == "up":
            post.upvotes += 1
        elif vote_type == "down":
            post.downvotes += 1
        else:
            return jsonify({'error': 'Invalid vote type'}), 400

        # Commit changes to the database
        db.session.commit()

        # Return updated vote counts
        return jsonify({'status': 'OK', 'upvotes': post.upvotes, 'downvotes': post.downvotes})

    except Exception as e:
        # Log the error and return a 500 response
        app.logger.error(f"Error processing vote: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500
