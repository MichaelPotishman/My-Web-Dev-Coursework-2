from app import db
from flask_login import UserMixin

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), index=True, unique=True)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500))
    password = db.Column(db.String(500))
    email = db.Column(db.String(1000))
    date_of_birth = db.Column(db.Date)

    # references to other tables
    posts = db.relationship('Posts', back_populates='user')
    likes = db.relationship('Likes', backref='user', lazy='dynamic')
    comments = db.relationship('Comments', backref='user', lazy='dynamic')


    followers = db.relationship('Followers', foreign_keys='Followers.follower_id', backref='followed_by', lazy='dynamic')
    following = db.relationship('Followers', foreign_keys='Followers.following_id', backref='following', lazy='dynamic')



    def __repr__(self):
        return f'<User {self.username}>'

class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
    upvotes = db.Column(db.Integer, default=0)

    # References
    likes = db.relationship('Likes', backref='posts', lazy='dynamic')
    comments = db.relationship('Comments', backref='posts', lazy='dynamic')
    user = db.relationship('User', back_populates='posts')
    
    # Relationship for hashtags via the PostHashtag association table
    hashtags = db.relationship('Hashtags', secondary='post_hashtag', back_populates='posts')

    def __repr__(self):
        return f'<Post {self.content[:20]}>'


class Likes(db.Model):
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))

    def __repr__(self):
        return f'<Like user_id={self.user_id} post_id={self.post_id}>'

class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))

    def __repr__(self):
        return f'<Comment user_id={self.user_id} post_id={self.post_id} content="{self.content[:20]}">'

class Followers(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return f'<Follower follower_id={self.follower_id}, followed_id={self.following_id}>'

class PostHashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtags.id'), nullable=False)

    # No additional relationships here; handled in Posts and Hashtags models

    def __repr__(self):
        return f'<PostHashtag post_id={self.post_id} hashtag_id={self.hashtag_id}>'

class Hashtags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relationship for posts via the PostHashtag association table
    posts = db.relationship('Posts', secondary='post_hashtag', back_populates='hashtags')

    def __repr__(self):
        return f'<Hashtag {self.name}>'