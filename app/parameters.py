import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB = os.getenv('DB')
COLLECTION = os.getenv('COLLECTION')