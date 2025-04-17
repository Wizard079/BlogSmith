import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = os.getenv('DEBUG')
NEWSDATA_IO_API_KEY = os.getenv('NEWSDATA_IO_API_KEY')