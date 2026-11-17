from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///sqlite.db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(bind=engine,
                expire_on_commit=False)
