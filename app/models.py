from app import db
import sqlalchemy as so
import sqlalchemy.orm as so
from typing import Optional

class User(db.Model):
    id: so.Mapped[int] = so.mappepd_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(16), index=True)
    lastname: so.Mapped[str] = so.mapped_column(sa.String(16), index=True)
    jobtitle: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    team: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    department: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)