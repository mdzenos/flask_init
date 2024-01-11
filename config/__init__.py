import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class Config:

    # Config FLASK_ENV
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    # Biến DEBUG
    DEBUG = os.getenv('DEBUG', 'False')

    # Cấu hình SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{os.getenv('DB_USERNAME')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cấu hình cho Alembic (Migrate)
    ALEMBIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migrations')
    ALEMBIC_CONFIG = os.path.join(ALEMBIC_DIR, 'alembic.ini')