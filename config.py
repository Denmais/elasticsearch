import os

DATABASE_URL = os.getenv("POSTGRES",
                         "postgresql+asyncpg://async_user:async_password@localhost:5432/async_jobs")

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "documents")