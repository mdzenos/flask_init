from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime,  server_default=func.now(), onupdate=func.now())
    deleted_at = db.Column(db.DateTime)

# # Import models vào package
from .users import Users
