import os

from flask import Flask
from app.routes import routes


PORT = int(os.environ.get('PORT', 5000))

app = Flask (__name__)

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(port=PORT)
