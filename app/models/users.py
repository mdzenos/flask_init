from app.models import BaseModel, db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from common.encrypt import PassWordManager

class Users(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(500))
    expired = db.Column(db.DateTime)

    def __repr__(self):
        return f"<User {self.username}>"

    def get_all(self):
        return Users.query.all()
    @classmethod
    def get_user(cls, username, access_token):
        return cls.query.filter(
            cls.birthday == username,
            cls.access_token == access_token
        ).first()

    @classmethod
    def create(cls, fullname, username, email, password):
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=engine)

        with Session.begin() as session:
            new_user = (Users(fullname=fullname, username=username, email=email, password=PassWordManager.hash_password(password)))
            session.add(new_user)
            session.commit()
        return new_user

    @classmethod
    def store(cls, username, password):
        pass

    @classmethod
    def check_login(cls, username, password):
        pass
