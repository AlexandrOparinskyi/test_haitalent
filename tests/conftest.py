import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.database import Base, get_async_session
from app.main import app


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:"
    )

    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def application(session):
    async def override_async_session():
        yield session

    app.dependency_overrides[get_async_session] = override_async_session
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(application):
    async with AsyncClient(
        transport=ASGITransport(app=application),
        base_url="http://test"
    ) as client:
        yield client
