from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"
engine = create_engine(db_url)

db_session = sessionmaker(autocommit=False,autoflush=False,bind=engine)