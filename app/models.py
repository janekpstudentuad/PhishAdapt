# Import required libraries
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash # For use in User model
from hashlib import md5 # For use in User model
from time import time # For use in User model
import jwt # For use in User model
from flask import current_app # For use in User model
from datetime import datetime # For use in User model

# Import classes from other functions
from app import db, login

# Create User class
class User(UserMixin, db.Model):
    # Set data types for db entries
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(16), index=True)
    lastname: so.Mapped[str] = so.mapped_column(sa.String(16), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    jobtitle: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    team: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    department: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    is_admin: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    
    # Map relationship to profile table
    profile: so.Mapped["Profile"] = relationship(back_populates="user", uselist=False)
    # Map relationship to campaign_results table
    campaign_results: so.Mapped[List["CampaignResult"]] = relationship(back_populates="user")

    # Method to set user password
    def set_password(self, password):
        # Generate password hash for insertion to db
        self.password_hash = generate_password_hash(password)

    # Method to check user password
    def check_password(self, password):
        # Check provided password hash against hash held in db
        return check_password_hash(self.password_hash, password)

    # Set string representation of for object
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # Method to display user avatar
    def avatar(self, size):
        # Generate MD5 hash of user email address
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        # Generate avatar using hashed email address. Third party service
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    # Method to generate JWT token for user self-service reset password function
    def get_reset_password_token(self, expires_in=600):
        # Generate JWT token
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    # Class method to verify valdity of a user reset JWT token
    @staticmethod
    def verify_reset_password_token(token):
        # Decode JWT, verify decoded contents match format for encoding the original token
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        # Skip functionality if JWT does not match encoding format
        except:
            return
        # Instantiate a User object with user information from db if decoded JWT matches encoding format
        return db.session.get(User, id)

# User login function
@login.user_loader
def load_user(id):
    # Instantiate a User object with user information from db
    return db.session.get(User, int(id))

# Create Organisation (for team/department info) class
class Organisation(db.Model):
    # Set data types for db entries
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    department: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    team: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)

# Create Profile class
class Profile(db.Model):
    # Set data types for db entries
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True, unique=True)
    user: so.Mapped["User"] = relationship(back_populates="profile")
    instructor: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    group: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    game: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    elearn: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    quiz: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    demo: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    video: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    text: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    visual: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    coach: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    audio: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    risk: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)

# Create Campaign class
class Campaign(db.Model):
    # Set data types for db entries
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    sent_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.now)

    # Map relationship to campaign result table
    results: so.Mapped[List["CampaignResult"]] = relationship(back_populates="campaign", cascade="all, delete-orphan")

# Create CampaignResult class
class CampaignResult(db.Model):
    # Set data types for db entries
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    campaign_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('campaign.id'), index=True, nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id", name="fk_campaign_result_user_id"), nullable=False)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    clicked: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    # Map relationship to campaign table
    campaign: so.Mapped["Campaign"] = relationship(back_populates="results")
    # Map relationship to user table
    user: so.Mapped["User"] = relationship(back_populates="campaign_results")