from flask import Flask
from .api.users import 
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.register_blueprint(userRouter, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(port=os.getenv('APP_PORT'))
