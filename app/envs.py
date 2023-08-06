import os

DB_URI = os.getenv("DB_URI")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 5))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", 2))
MAX_NUMBER_THREADS = int(os.getenv("MAX_NUMBER_THREADS", 5))
