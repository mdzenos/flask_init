from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime,  server_default=func.now(), onupdate=func.now())
    deleted_at = db.Column(db.DateTime)

    def to_dict(self):
        obj_dict = {key: self.format_datetime(getattr(self, key))
                    if isinstance(getattr(self, key), datetime) else getattr(self, key)
                    for key in dir(self) if not key.startswith('_') and not callable(getattr(self, key))}
        excluded_keys = ['registry', 'query', 'metadata']
        obj_dict = {key: value for key, value in obj_dict.items()
                    if key not in excluded_keys and (not isinstance(value, datetime) or isinstance(value, datetime) and value is not None)}
        return obj_dict

    def format_datetime(self, value):
        return value.strftime('%Y-%m-%d %H:%M:%S') if value else None

# # Import models vào package
from .users import Users
