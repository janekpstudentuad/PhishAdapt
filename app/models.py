from app import db, login
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import relationship
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt
from flask import current_app
from sqlalchemy import CheckConstraint

class User(UserMixin, db.Model):
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
    profile: so.Mapped["Profile"] = relationship(back_populates="user", uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)
    
    def get_training_token(self, expires_in=604800):
        return jwt.encode({'clicked': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_training_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['clicked']
        except:
            return
        return db.session.get(User, id)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Organisation(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    department: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    team: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)

class Profile(db.Model):
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