from app import create_app
from config import Config

app = create_app()

if __name__ == "__main__":
    app.run(
        debug=Config.DEBUG,
        host='0.0.0.0',
        port=8888,
        # load_dotenv=True
        # use_reloader=False
        # threaded=True,
        # processes=4,
        # ssl_context=('cert.pem', 'key.pem')
    )