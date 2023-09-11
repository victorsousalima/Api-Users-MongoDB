import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
DB = os.getenv('DB')
COLLECTION = os.getenv('COLLECTION')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')