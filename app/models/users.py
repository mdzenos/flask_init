from sqlalchemy.exc import SQLAlchemyError
from common.exceptions import DatabaseException
from app.models import BaseModel, db
from datetime import datetime
from common.encrypt import PassWordManager, JWTAppManager
from flask import jsonify


class Users(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    ref_token = db.Column(db.String(500))
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Users id={self.id}, fullname={self.fullname}, username={self.username}, email={self.email} >'

    def __init__(self, fullname, username, password, email):
        self.fullname = fullname
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def create(cls, fullname, username, password, email):
        try:
            new_user = cls(
                fullname=fullname,
                username=username,
                password=PassWordManager.hash_password(password),
                email=email
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            raise DatabaseException(e)

    @staticmethod
    def get_user(username=None, id=None):
        if username is not None:
            get_user = Users.query.filter_by(username=username, is_deleted=False).first()
            if get_user is None:
                return None
            return get_user
        elif id is not None:
            get_user = Users.query.filter_by(id=id, is_deleted=False).first()
            if get_user is None:
                return None
            return get_user
        return None

    @staticmethod
    def get_all_user():
        return Users.query.filter(Users.is_deleted == False).all()

    @staticmethod
    def update(id=None, fullname=None, username=None, password=None, email=None, ref_token=None):
        user = Users.get_user(id=id)
        try:
            if user:
                if fullname is not None:
                    user.fullname = fullname
                if username is not None:
                    user.username = username
                if password is not None:
                    user.password = PassWordManager.hash_password(password)
                if email is not None:
                    user.email = email
                if ref_token is not None:
                    user.ref_token = ref_token
                db.session.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            raise DatabaseException(e)

    @classmethod
    def delete_user(cls, user_id):
        try:
            user = Users.get_user(id=user_id)
            if user is not None:
                user.is_deleted = True
                user.deleted_at = datetime.utcnow()
                db.session.commit()
                return user.username
            return None
        except SQLAlchemyError as e:
            raise DatabaseException(e)

    @staticmethod
    def save_new_token(user_id):
        access_token = JWTAppManager.create_access_token(user_id)
        refresh_token = JWTAppManager.create_refresh_token(user_id)
        if access_token is not None and refresh_token is not None:
            saved_token = Users.update(id=user_id, ref_token=refresh_token)
            if saved_token is not None:
                return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
        return None
